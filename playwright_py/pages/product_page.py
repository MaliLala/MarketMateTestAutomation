# playwright_py/pages/product_page.py
# ------------------------------------------------------------
# ProductPage – mirrors Selenium ProductPage
# Handles product detail view: quantity, Add to Cart, reviews
# ------------------------------------------------------------

from playwright.sync_api import Page
from .login_page import LoginPage
from .checkout_page import CheckoutPage

BASE_URL = "https://grocerymate.masterschool.com"

class ProductPage:
    def __init__(self, page: Page):
        self.page = page

    # --- Assertions / State ---
    def is_displayed(self) -> bool:
        """Check if current page is a product detail page."""
        return "/product/" in self.page.url

    # --- Actions ---
    def set_quantity(self, value: int = 1):
        """Set product quantity if input exists."""
        qty = self.page.locator("input[type='number'], input[class*='quantity']").first
        if qty.count() and qty.is_visible():
            qty.fill(str(value))
        return self

    def add_to_cart(self):
        """Click 'Add to Cart' and handle redirect."""
        add_btn = self.page.locator("button.btn-cart").first
        if not add_btn.count():
            raise AssertionError("No 'Add to Cart' button found on product page")
        add_btn.scroll_into_view_if_needed()
        add_btn.click()

        if self.page.url.startswith(f"{BASE_URL}/auth"):
            return LoginPage(self.page)
        if self.page.url.startswith(f"{BASE_URL}/checkout"):
            return CheckoutPage(self.page)
        return self

    def open_reviews_tab(self):
        """If product has reviews tab, click it."""
        tab = self.page.locator("text=/review/i").first
        if tab.count() and tab.is_visible():
            tab.click()
        return self

    def has_price(self) -> bool:
        """Return True if a price element is visible."""
        sel = self.page.locator("text=/€|price|total/i").first
        return sel.count() > 0 and sel.is_visible()

