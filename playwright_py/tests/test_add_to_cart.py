import os
import re
import pytest
from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from pages.checkout_page import CheckoutPage

pytestmark = pytest.mark.e2e

BASE = "https://grocerymate.masterschool.com"
EMAIL = os.getenv("USER_EMAIL")
PASSWORD = os.getenv("USER_PASSWORD")

@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="USER_EMAIL/USER_PASSWORD not set in .env")
def test_add_to_cart_then_open_cart(page):
    """
    GIVEN a logged-in user
    WHEN they add the first product on /store and click the cart icon
    THEN the checkout/cart view opens and shows at least one item
    """

    # 1) Login (same as Selenium’s LoginPage usage)
    page.goto(f"{BASE}/auth", wait_until="domcontentloaded")
    LoginPage(page).login(EMAIL, PASSWORD)

    # 2) Go to /store and pass age modal (ShopPage handles this)
    shop = ShopPage(page).open()

    # 3) Add first product from the grid
    result = shop.add_first_product()

    # 4) Click the cart icon in the header (don’t hard-jump to /checkout)
    # Try direct link first, then fall back to a11y name that contains "cart"
    banner = page.get_by_role("banner")
    cart_link = banner.locator('a[href="/checkout"]').first
    if cart_link.count() == 0:
        cart_link = banner.get_by_role("link", name=re.compile(r"cart|shopping", re.I)).first

    assert cart_link.count() > 0 and cart_link.is_visible(), "Cart icon/link not found in header"
    cart_link.click()

    # 5) Assert we’re on the cart/checkout and there’s at least one line item
    checkout = CheckoutPage(page)
    assert checkout.is_displayed(), "Checkout/cart page did not open after clicking cart icon"
    assert checkout.has_items(), "Expected at least one item in the cart"
