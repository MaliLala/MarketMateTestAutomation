# playwright_py/pages/shop_page.py
# ------------------------------------------------------------
# ShopPage – mirrors Selenium ShopPage
# Opens /store, passes age modal, adds product to cart,
# redirects to LoginPage if unauthenticated.
# ------------------------------------------------------------

import re
from playwright.sync_api import Page, TimeoutError as PWTimeout
from .login_page import LoginPage
from .checkout_page import CheckoutPage
from .product_page import ProductPage

BASE_URL = "https://grocerymate.masterschool.com"

class ShopPage:
    def __init__(self, page: Page):
        self.page = page

    # --- Navigation ---
    def open(self):
        """Open the /store page and handle age verification."""
        self.page.goto(f"{BASE_URL}/store", wait_until="domcontentloaded")
        self._pass_age_modal()
        return self

    # --- Internal helpers ---
    def _pass_age_modal(self):
        """Fill DOB if modal appears."""
        try:
            dob = self.page.get_by_placeholder("DD-MM-YYYY")
            if dob.count() and dob.first.is_visible():
                dob.first.fill("01-01-1990", timeout=2000)
                self.page.get_by_role("button", name=re.compile("confirm", re.I)).click(timeout=2000)
                self.page.wait_for_timeout(300)
        except Exception:
            pass

    def _wait_for_products(self):
        """Scroll down until product cards or buttons appear."""
        for _ in range(4):
            try:
                self.page.wait_for_selector("button.btn-cart", state="visible", timeout=1000)
                return
            except PWTimeout:
                self.page.evaluate("window.scrollBy(0, window.innerHeight * 0.5)")
                self.page.wait_for_timeout(200)

    # --- Actions ---
    def add_first_product(self):
        """Click first Add-to-Cart button and handle redirects."""
        self._wait_for_products()
        add_btn = self.page.locator("button.btn-cart").first
        if not add_btn.count():
            raise AssertionError("No 'Add to Cart' button found")

        add_btn.scroll_into_view_if_needed()
        add_btn.click()

        # Redirection handling
        if self.page.url.startswith(f"{BASE_URL}/auth"):
            return LoginPage(self.page)
        if self.page.url.startswith(f"{BASE_URL}/checkout"):
            return CheckoutPage(self.page)
        return self

    def open_first_product(self):
        """Open first product card link to reach ProductPage."""
        link = self.page.locator("a[href^='/product/']").first
        if not link.count():
            raise AssertionError("No product link found")
        link.click()
        return ProductPage(self.page)

    def go_to_checkout(self):
        """Navigate directly to checkout."""
        self.page.goto(f"{BASE_URL}/checkout", wait_until="domcontentloaded")
        return CheckoutPage(self.page)
