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


@pytest.mark.order(7)
@pytest.mark.usefixtures('driver', 'config')
def test_4_star_review_submission(driver, config):
    """
    Submit a 4-star review after purchasing a product.
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

    # Step 5: Submit 4-star review
    product_page.remove_existing_review()
    comment = f"AutoTestG - 4★ review - {uuid4().hex[:6]}"
    product_page.select_star_rating(4)
    product_page.enter_review_text(comment)
    product_page.submit_review()

    # Step 6: Validate review
    time.sleep(2)
    username = "AutoTestG"
    assert product_page.user_has_comment(username), f"No review found for user '{username}'"

    # Step 7: Clean up cart
    CheckoutCleaner(driver).clear_cart()
