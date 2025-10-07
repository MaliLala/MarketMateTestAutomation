import pytest

pytestmark = pytest.mark.smoke

HOME_URL = "https://grocerymate.masterschool.com/"

def _handle_age_verification_if_present(page):
    """
    If the age/DOB modal is present on /store, fill a valid date (DD-MM-YYYY) and confirm.
    This mirrors Selenium ShopPage.handle_age_verification(dob).
    """
    try:
        # Look for the DOB input by placeholder
        dob = page.get_by_placeholder("DD-MM-YYYY")
        if dob.count() > 0 and dob.first.is_visible():
            dob.first.fill("01-01-1990", timeout=2000)
            # Confirm button with text 'Confirm'
            page.get_by_role("button", name="Confirm").click(timeout=2000)
            # brief settle
            page.wait_for_timeout(500)
    except Exception:
        # best-effort only; don't fail if the modal isn't present
        pass

def test_product_page_loads_and_has_content(page):
    """
    GIVEN the user opens the site
    WHEN they navigate to the Store and pass age verification
    THEN at least one product card is visible with an Add to cart control
    """
    # 1) Home
    resp = page.goto(HOME_URL, wait_until="domcontentloaded")
    assert resp is not None and resp.ok, f"Home navigation failed: {resp.status if resp else 'no response'}"

    # 2) /store
    origin = page.evaluate("() => location.origin")
    store_url = origin + "/store"
    resp2 = page.goto(store_url, wait_until="domcontentloaded")
    assert resp2 is not None and resp2.ok, f"Store navigation failed: {resp2.status if resp2 else 'no response'}"

    # 2a) Handle the age verification modal if it appears (DD-MM-YYYY + Confirm)
    try:
        dob = page.get_by_placeholder("DD-MM-YYYY")
        if dob.count() > 0 and dob.first.is_visible():
            dob.first.fill("01-01-1990", timeout=2000)
            page.get_by_role("button", name="Confirm").click(timeout=2000)
            page.wait_for_timeout(400)
    except Exception:
        pass

    # 3) Assert there is at least one product card on the page
    # Try common hooks the Selenium version relied on: quantity input and add-to-cart button in a card
    qty_input = page.locator("input.quantity")
    add_btn = page.locator("button.btn-cart")

    # If not immediately present, allow a brief hydrate/scroll (lazy grids)
    if qty_input.count() == 0 or add_btn.count() == 0:
        page.wait_for_timeout(400)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(400)

    assert qty_input.count() > 0, "No product quantity input found on Store page"
    assert add_btn.count() > 0, "No 'Add to cart' button found on Store page"

    # Optional: verify the first card’s controls are visible
    assert qty_input.first.is_visible(), "Quantity input is not visible"
    assert add_btn.first.is_visible(), "Add to cart button is not visible"
