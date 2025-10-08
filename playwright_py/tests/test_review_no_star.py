import os
import re
import pytest
from pages.login_page import LoginPage
from pages.shop_page import ShopPage

pytestmark = pytest.mark.e2e

EMAIL = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")

@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="USER_EMAIL/USER_PASSWORD not set")
def test_review_no_star(page):
    """
    GIVEN a logged-in user on a product review form
    WHEN they submit text without selecting a star rating
    THEN a validation message is shown
    """
    page.goto("https://grocerymate.masterschool.com/auth", wait_until="domcontentloaded")
    LoginPage(page).login(EMAIL, PASSWORD)

    ShopPage(page).open().open_first_product().open_reviews_tab()

    textarea = page.get_by_role("textbox").first
    textarea.fill("Forgot to pick a star…")
    submit = page.get_by_role("button", name=re.compile(r"submit", re.I)).first
    submit.click()

    # TODO: adjust to your validation text
    validation = page.locator("text=/select a rating|please choose a rating|required/i").first
    assert validation.count() > 0, "Expected a 'rating required' validation message"
