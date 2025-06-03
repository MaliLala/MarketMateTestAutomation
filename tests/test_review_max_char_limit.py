# tests/test_review_max_char_limit.py

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage
from pages.shop_page import ShopPage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage
from pages.checkout_cleaner import CheckoutCleaner


@pytest.mark.order(6)
@pytest.mark.xfail(reason="Submit button is incorrectly enabled at 500/500 chars", strict=True)
@pytest.mark.usefixtures("driver", "config")
def test_review_max_character_limit(driver, config):
    """
    Verify that the product review comment field enforces a 500 character limit
    and displays a warning when the user hits the max length.
    """

    wait = WebDriverWait(driver, 20)

    # Step 1: Login and age verification
    LoginPage(driver).login(config["email"], config["password"])
    age = AgeVerificationPage(driver)
    age.open_shop()
    age.enter_dob("08-08-2000")
    age.confirm_age()

    # Step 2: Select product
    shop_page = ShopPage(driver)
    product_element = shop_page.get_first_product_card()
    input_elem = product_element.find_element(By.CSS_SELECTOR, "input.quantity")
    product_id = input_elem.get_attribute("name").split("_", 1)[1]

    # Step 3: Add to cart and purchase
    shop_page.add_first_product_to_cart()
    time.sleep(1.5)
    checkout = CheckoutPage(driver)
    checkout.buy()

    # Step 4: Open product page
    shop_page.open_store()
    product_page = ProductPage(driver)
    product_page.load(product_id)
    product_page.remove_existing_review()

    # Step 5: Generate and input over-limit comment
    long_text = "X" * 600  # Deliberately exceeds max of 500
    product_page.select_star_rating(5)

    textarea = driver.find_element(By.CSS_SELECTOR, "textarea.new-review-form-control")
    textarea.clear()
    textarea.send_keys(long_text)

    # Step 6: Check actual length of entered text
    entered_text = textarea.get_attribute("value")
    print(f"Entered characters: {len(entered_text)}")
    assert len(entered_text) == 500, "Field did not enforce 500 character limit"

    # Step 7: Check for warning message
    warning = driver.find_element(By.CSS_SELECTOR, ".error-message")
    assert "You cannot tell us more about this product" in warning.text, "Expected warning not displayed"

    # Step 8: Ensure submission is disabled
    send_button = driver.find_element(By.CSS_SELECTOR, ".new-review-btn-send")
    assert not send_button.is_enabled(), "Submit button should be disabled at 500/500 chars"

    # Step 9: Cleanup
    CheckoutCleaner(driver).clear_cart()
