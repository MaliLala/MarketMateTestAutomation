import time
import pytest
from uuid import uuid4
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage
from pages.shop_page import ShopPage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage
from pages.checkout_cleaner import CheckoutCleaner


@pytest.mark.order(8)  # Or adjust the order as needed
@pytest.mark.usefixtures('driver', 'config')
def test_review_no_star_submission(driver, config):
    """
    Submit a review without selecting any star rating after purchasing a product.
    Verify that the system blocks the submission and no review is saved.
    """

    wait = WebDriverWait(driver, 20)

    # Step 1: Log in and pass age gate
    LoginPage(driver).login(config["email"], config["password"])
    age = AgeVerificationPage(driver)
    age.open_shop()
    age.enter_dob("08-08-2000")
    age.confirm_age()

    # Step 2: Select first product
    shop_page = ShopPage(driver)
    product_element = shop_page.get_first_product_card()
    input_elem = product_element.find_element(By.CSS_SELECTOR, "input.quantity")
    product_id = input_elem.get_attribute("name").split("_", 1)[1]

    # Step 3: Add to cart and buy
    shop_page.add_first_product_to_cart()
    time.sleep(1.5)

    checkout = CheckoutPage(driver)
    checkout.buy()

    # Step 4: Load product page directly by ID
    shop_page.open_store()
    product_page = ProductPage(driver)
    product_page.load(product_id)

    # Step 5: Attempt to submit a review without selecting stars
    product_page.remove_existing_review()
    comment = f"AutoTestG - no star review - {uuid4().hex[:6]}"
    # Do NOT select any stars here
    product_page.enter_review_text(comment)
    product_page.submit_review()

    # Step 6: Validate no review saved and error handling
    time.sleep(2)
    username = "AutoTestG"
    # Assert the user does NOT have a saved comment, since submission should be blocked
    assert not product_page.user_has_comment(username), f"Unexpected review found for user '{username}'"

    # Optionally, you can check for the presence of an error message about rating being required here
    # e.g. wait for error toast or message

    # Step 7: Clean up cart
    CheckoutCleaner(driver).clear_cart()
