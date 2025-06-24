import time
import pytest
from uuid import uuid4
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage


@pytest.mark.usefixtures('driver', 'config')
def test_4_star_review_submission(driver, config):
    """
    Submit a 4-star review after purchasing a product.
    """

    wait = WebDriverWait(driver, 20)

    # Step 1: Log in and wait for main store URL
    LoginPage(driver).login(config["email"], config["password"])
    wait.until(EC.url_to_be("https://grocerymate.masterschool.com/"))

    # Step 2: Open store page and handle age verification
    shop_page = ShopPage(driver)
    shop_page.open_store()
    shop_page.handle_age_verification("08-08-2000")

    # Step 3: Select first product and extract product ID
    product_element = shop_page.get_first_product_card()
    input_elem = product_element.find_element(By.CSS_SELECTOR, "input.quantity")
    product_id = input_elem.get_attribute("name").split("_", 1)[1]

    # Step 4: Add product to cart and purchase
    shop_page.add_first_product_to_cart()
    time.sleep(1.5)

    checkout = CheckoutPage(driver)
    checkout.buy()

    # Step 5: Navigate to product page by ID
    shop_page.open_store()
    product_page = ProductPage(driver)
    product_page.load(product_id)

    # Step 6: Submit 4-star review with unique comment
    product_page.remove_existing_review()
    comment = f"AutoTestG - 4-star review - {uuid4().hex[:6]}"
    product_page.select_star_rating(4)
    product_page.enter_review_text(comment)
    product_page.submit_review()

    # Step 7: Validate review presence
    time.sleep(2)
    username = "AutoTestG"
    assert product_page.user_has_comment(username), f"No review found for user '{username}'"

    # Step 8: Clear cart after test
    checkout.clear_cart()
