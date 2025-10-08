import os
import pytest
from pages.login_page import LoginPage
from pages.shop_page import ShopPage

pytestmark = pytest.mark.e2e

EMAIL = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")

@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="USER_EMAIL/USER_PASSWORD not set")
def test_review_max_char_limit(page):
    """
    GIVEN a logged-in user on a product review form
    WHEN they enter a very long review
    THEN the UI prevents input beyond max length or shows a validation message
    """
    page.goto("https://grocerymate.masterschool.com/auth", wait_until="domcontentloaded")
    LoginPage(page).login(EMAIL, PASSWORD)

    ShopPage(page).open().open_first_product().open_reviews_tab()

    # TODO: set to your actual max length (e.g., 300/500)
    long_text = "x" * 1000
    textarea = page.get_by_role("textbox").first
    assert textarea.count() > 0, "Review textarea not found"
    textarea.fill(long_text)

    # Heuristic check: content length clipped or error shown
    val = textarea.input_value()
    too_long = len(val) > 600  # adjust threshold if needed
    error = page.locator("text=/too long|max/i").first
    assert len(val) < 1000 or error.count() > 0, "No char limit enforcement (adjust selector/limit)"
