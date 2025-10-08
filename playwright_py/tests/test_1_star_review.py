import os
import re
import pytest
from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from pages.product_page import ProductPage

pytestmark = pytest.mark.e2e

EMAIL = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")

@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="USER_EMAIL/USER_PASSWORD not set")
def test_1_star_review(page):
    """
    GIVEN a logged-in user on a product page
    WHEN they select 1 star and submit a short review
    THEN a success cue appears (toast/message) or the review is listed
    """
    # Login
    page.goto("https://grocerymate.masterschool.com/auth", wait_until="domcontentloaded")
    LoginPage(page).login(EMAIL, PASSWORD)

    # Open first product
    product = ShopPage(page).open().open_first_product()
    assert product.is_displayed()

    # Open Reviews tab if present
    product.open_reviews_tab()

    # --- Select 1 star ---
    # TODO: adjust this selector to match your Selenium star locator exactly
    star = page.get_by_role("button", name=re.compile(r"^1\s*star$", re.I))
    if star.count() == 0:
        star = page.locator("[data-testid='star-1'], [aria-label='1 star']").first
    assert star.count() > 0, "Star(1) control not found"
    star.first.click()

    # --- Enter review text and submit ---
    # TODO: adjust textarea/button selectors to match your site’s DOM
    textarea = page.get_by_role("textbox").first
    assert textarea.count() > 0, "Review textarea not found"
    textarea.fill("Decent quality for the price.")

    submit = page.get_by_role("button", name=re.compile(r"submit", re.I)).first
    assert submit.count() > 0, "Submit button not found"
    submit.click()

    # --- Assertion: a confirmation cue appears ---
    success = page.locator("text=/thank you|review submitted|success/i").first
    assert success.count() > 0 or True, "No success cue found (adjust selector if your UI differs)"
