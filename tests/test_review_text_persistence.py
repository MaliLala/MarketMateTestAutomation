# tests/test_review_text_persistence.py

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


@pytest.mark.order(5)
@pytest.mark.xfail(reason="Review comment not persisted — known issue", strict=True)
@pytest.mark.usefixtures('driver', 'config')
def test_review_text_persistence(driver, config):
    """
    Submits a review with star and comment, refreshes the page, and asserts the comment is preserved.
    This test is expected to FAIL if the system does not persist review text.
    """

    wait = WebDriverWait(driver, 20)

    # Step 1: Login and pass age check
    LoginPage(driver).login(config["email"], config["password"])
    age = AgeVerificationPage(driver)
    age.open_shop()
    age.enter_dob("08-08-2000")
    age.confirm_age()

    # Step 2: Get product ID
    shop_page = ShopPage(driver)
    product_element = shop_page.get_first_product_card()
    input_elem = product_element.find_element(By.CSS_SELECTOR, "input.quantity")
    product_id = input_elem.get_attribute("name").split("_", 1)[1]

    # Step 3: Add to cart and buy
    shop_page.add_first_product_to_cart()
    time.sleep(1.5)

    checkout = CheckoutPage(driver)
    checkout.buy()

    # Step 4: Load product page
    shop_page.open_store()
    product_page = ProductPage(driver)
    product_page.load(product_id)

    # Step 5: Submit review with text
    product_page.remove_existing_review()
    comment = f"AutoTestG - text-persist - {uuid4().hex[:6]}"
    product_page.select_star_rating(3)
    product_page.enter_review_text(comment)
    product_page.submit_review()

    time.sleep(2)
    driver.refresh()
    product_page.load(product_id)

    # Step 6: Assert that the review text still exists
    reviews = product_page.get_review_comments()
    assert any(comment in r for r in reviews), "Review comment text not found after refresh!"

    # Step 7: Clean up
    CheckoutCleaner(driver).clear_cart()
