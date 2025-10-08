import os
import pytest
from pages.login_page import LoginPage

pytestmark = pytest.mark.e2e

EMAIL = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")

@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="USER_EMAIL/USER_PASSWORD not set")
def test_login_flow(page):
    """
    GIVEN the login page
    WHEN valid credentials are submitted
    THEN the user lands on the Store (/store)
    """
    login = LoginPage(page)
    page.goto("https://grocerymate.masterschool.com/auth", wait_until="domcontentloaded")

    login.login(EMAIL, PASSWORD)
    assert page.url.startswith("https://grocerymate.masterschool.com/store"), "Login did not reach /store"
