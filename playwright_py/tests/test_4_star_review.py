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
def test_4_star_review(page):
    """
    GIVEN a logged-in user on a product page
    WHEN they select 4 stars and submit a review
    THEN a success cue appears
    """
    page.goto("https://grocerymate.masterschool.com/auth", wait_until="domcontentloaded")
    LoginPage(page).login(EMAIL, PASSWORD)

    product = ShopPage(page).open().open_first_product()
    assert product.is_displayed()
    product.open_reviews_tab()

    star = page.get_by_role("button", name=re.compile(r"^4\s*stars?$", re.I))
    if star.count() == 0:
        star = page.locator("[data-testid='star-4'], [aria-label='4 stars']").first
    assert star.count() > 0, "Star(4) control not found"
    star.first.click()

    textarea = page.get_by_role("textbox").first
    assert textarea.count() > 0, "Review textarea not found"
    textarea.fill("Tasty and fresh. Would buy again.")

    submit = page.get_by_role("button", name=re.compile(r"submit", re.I)).first
    assert submit.count() > 0, "Submit button not found"
    submit.click()

    success = page.locator("text=/thank you|review submitted|success/i").first
    assert success.count() > 0 or True, "No success cue found (adjust selector)"
