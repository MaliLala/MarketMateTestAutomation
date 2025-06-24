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

def is_logged_in(driver):
    # Adjust cookie name if your app uses a different one for session
    return driver.get_cookie("session") is not None

def test_1_star_review_submission(driver, config):
    """
    Submit a 1-star review after purchasing a product.
    """

    wait = WebDriverWait(driver, 20)

    # Step 1: Log in and pass age gate
    LoginPage(driver).login(config["email"], config["password"])
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_to_be("https://grocerymate.masterschool.com/"))

    shop_page = ShopPage(driver)
    shop_page.open_store()

    shop_page.handle_age_verification("08-08-2000")

    # Step 2: Select first product
    product_element = shop_page.get_first_product_card()
    input_elem = product_element.find_element(By.XPATH, ".//input[contains(@class, 'quantity')]")
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

    # Step 5: Submit 1-star review
    product_page.remove_existing_review()
    comment = f"AutoTestG - 1 Star review - {uuid4().hex[:6]}"
    product_page.select_star_rating(1)
    product_page.enter_review_text(comment)
    product_page.submit_review()

    # Step 6: Validate review
    time.sleep(2)
    username = "AutoTestG"
    assert product_page.user_has_comment(username), f"No review found for user '{username}'"

    # Step 7: Clean up cart
    CheckoutPage(driver).clear_cart()

