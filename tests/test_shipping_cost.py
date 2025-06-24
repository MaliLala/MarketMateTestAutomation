import math  # Used to calculate required quantity to exceed €20
import time  # Used for sleep pauses between actions
import pytest  # PyTest framework and decorators
from selenium.webdriver.support.ui import WebDriverWait  # For explicit waits
from selenium.webdriver.support import expected_conditions as EC  # For Selenium wait conditions

# Import page modules
from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from pages.checkout_page import CheckoutPage


@pytest.mark.usefixtures("driver", "config")
#@pytest.mark.xfail(reason="Shipping does not update to €5 when subtotal drops below €20")
def test_shipping_cost_threshold(driver, config):
    """
    Steps:
    1. Log in
    2. Pass age gate
    3. Add enough quantity to exceed €20 → expect free shipping
    4. Decrease quantity until subtotal is below €20 → expect €5 shipping
    5. Clean up the cart
    """

    wait = WebDriverWait(driver, 20)  # General wait object

    # Step 1: Log in and pass age gate
    LoginPage(driver).login(config["email"], config["password"])

    # Step 2: Complete age verification flow
    shop_page = ShopPage(driver)
    shop_page.open_store()  # Navigate to store and wait for page/modal
    shop_page.handle_age_verification("08-08-2000")  # Enter DOB and confirm
    wait.until(EC.url_contains("/store"))  # Wait for URL to confirm we're on the store page

    # Step 3: Calculate how many items are needed to exceed €20
    shop_page.open_store()  # Navigate to the store
    unit_price = shop_page.get_first_product_price()  # Get price of first visible item
    qty = math.floor(20 / unit_price) + 1  # Compute minimum quantity to exceed €20

    # Step 4: Add calculated quantity of product to cart
    shop_page.add_first_product_to_cart(qty)  # Add that quantity to the cart
    time.sleep(2)  # Allow time for cart update

    # Step 5: Assert shipping cost is free
    checkout = CheckoutPage(driver)
    checkout.open_checkout()  # Navigate to checkout page
    shipping = checkout.read_shipping_cost()  # Read current shipping cost
    assert "0" in shipping or "Free" in shipping, f"Expected free shipping, got: {shipping}"

    # Step 6: Remove 1 item at a time until subtotal < €20
    while unit_price * qty >= 20:
        checkout.decrease_quantity()  # Click "-" button once
        qty -= 1  # Adjust tracked quantity down

    # Step 7: Check that shipping cost is now €5
    shipping = checkout.read_shipping_cost()
    assert "5" in shipping or "5.00" in shipping, f"Expected €5 shipping, got: {shipping}"  # This assert is known to fail

    # Step 8: Cleanup - remove all items from cart
    checkout.clear_cart()
