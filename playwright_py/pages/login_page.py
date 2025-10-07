# playwright_py/pages/login_page.py
# ------------------------------------------------------------
# LoginPage – mirrors Selenium LoginPage
# Handles login form interactions and login state verification
# ------------------------------------------------------------

from playwright.sync_api import Page

BASE_URL = "https://grocerymate.masterschool.com"

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    # --- Assertions / State ---
    def is_displayed(self) -> bool:
        """Check that the current URL is the login page."""
        return self.page.url.startswith(f"{BASE_URL}/auth")

    # --- Actions ---
    def login(self, email: str, password: str):
        """Fill in credentials and submit."""
        self.page.get_by_label("Email").fill(email)
        self.page.get_by_label("Password").fill(password)
        self.page.get_by_role("button", name="Login").click()
        self.page.wait_for_url(f"{BASE_URL}/store")
        return self

    def get_error_message(self) -> str:
        """Return visible error text if login fails."""
        el = self.page.locator("text=/invalid|wrong|failed/i").first
        return (el.text_content() or "").strip() if el.count() else ""
