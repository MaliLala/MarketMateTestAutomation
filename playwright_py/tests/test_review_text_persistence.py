import os
import pytest
from pages.login_page import LoginPage
from pages.shop_page import ShopPage

pytestmark = pytest.mark.e2e

EMAIL = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")

@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="USER_EMAIL/USER_PASSWORD not set")
def test_review_text_persistence(page):
    """
    GIVEN a logged-in user typing a review
    WHEN they navigate away and back (without submitting)
    THEN the typed text remains (if app supports draft persistence)
    """
    page.goto("https://grocerymate.masterschool.com/auth", wait_until="domcontentloaded")
    LoginPage(page).login(EMAIL, PASSWORD)

    ShopPage(page).open().open_first_product().open_reviews_tab()

    textarea = page.get_by_role("textbox").first
    assert textarea.count() > 0, "Review textarea not found"
    textarea.fill("Draft review text…")

    # Navigate away to Store and back (first product again)
    page.goto("https://grocerymate.masterschool.com/store", wait_until="domcontentloaded")
    ShopPage(page).open().open_first_product().open_reviews_tab()

    # Check if draft persisted
    val = page.get_by_role("textbox").first.input_value()
    assert val.strip() != "", "Draft review text did not persist (skip if feature not supported)"
