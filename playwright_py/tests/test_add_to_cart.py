import re
import pytest
from playwright.sync_api import TimeoutError as PWTimeout

pytestmark = pytest.mark.e2e

BASE = "https://grocerymate.masterschool.com"  # no trailing slash

def _pass_age_modal(page):
    """Best-effort: fill DOB 'DD-MM-YYYY' and click Confirm if shown."""
    try:
        dob = page.get_by_placeholder("DD-MM-YYYY")
        if dob.count() and dob.first.is_visible():
            dob.first.fill("01-01-1990", timeout=2000)
            page.get_by_role("button", name=re.compile(r"confirm", re.I)).click(timeout=2000)
            page.wait_for_timeout(300)
    except Exception:
        pass

def test_add_to_cart_minimal(page):
    """
    Minimal parity with Selenium Shop flow:
    - open /store
    - scroll to top
    - pass DOB modal
    - click the first 'Add to Cart' button
    """
    # open store
    page.goto(f"{BASE}/store", wait_until="domcontentloaded")

    # ensure we start at the top (your earlier run showed the footer)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(200)

    _pass_age_modal(page)

    # wait a bit for grid to hydrate; then look for the exact class you showed
    for _ in range(4):
        try:
            page.wait_for_selector("button.btn-cart", state="visible", timeout=1500)
            break
        except PWTimeout:
            # nudge lazy content
            page.evaluate("window.scrollBy(0, Math.floor(window.innerHeight*0.75))")
            page.wait_for_timeout(250)

    # click the first Add to Cart we can see
    add_btn = page.locator("button.btn-cart").first
    assert add_btn.count() > 0 and add_btn.is_visible(), "Couldn't find a visible 'Add to Cart' button"
    add_btn.scroll_into_view_if_needed()
    add_btn.click()

    # sanity: page is still interactive
    assert page.url.startswith(f"{BASE}/store"), f"Unexpected redirect after add: {page.url}"
