# playwright_py/pages/checkout_page.py
# ------------------------------------------------------------
# CheckoutPage – mirrors Selenium CheckoutPage
# Used to validate cart content and totals
# ------------------------------------------------------------

from playwright.sync_api import Page

BASE_URL = "https://grocerymate.masterschool.com"

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

    # --- Assertions / State ---
    def is_displayed(self) -> bool:
        """Return True if current URL is /checkout."""
        return self.page.url.startswith(f"{BASE_URL}/checkout")

    def has_items(self) -> bool:
        """Return True if the cart table/list has visible items."""
        selectors = [
            "[data-testid*='cart'] [data-testid*='item']",
            "[class*='cart'] [class*='item']",
            ".cart-item",
            "ul li[class*='item']",
            "table tr",
        ]
        for sel in selectors:
            loc = self.page.locator(sel)
            if loc.count() > 0 and loc.first.is_visible():
                return True
        return False

    def get_total_amount(self) -> str:
        """Return subtotal or total text from checkout."""
        loc = self.page.locator("text=/total|subtotal/i").first
        return (loc.text_content() or "").strip() if loc.count() else ""
