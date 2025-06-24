import time
import math
import pytest
import random

from uuid import uuid4
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from pages.product_page import ProductPage


@pytest.mark.usefixtures("driver", "config")
def test_average_rating_update(driver, config):
    """
    Submits a 4-star review and verifies that the average rating
    and review count update as expected.
    """
    wait = WebDriverWait(driver, 10)

    # Step 1: Log in and pass age gate
    LoginPage(driver).login(config["email"], config["password"])

    # Step 2: Age verification
    shop_page = ShopPage(driver)
    shop_page.open_store()
    shop_page.handle_age_verification("08-08-2000")  # Required for age gate
    time.sleep(1)

    # Step 3: Wait for product cards to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))

    # Step 4: Navigate to product
    product_element = shop_page.get_first_product_card()
    input_elem = product_element.find_element(By.CSS_SELECTOR, "input.quantity")
    product_id = input_elem.get_attribute("name").split("_", 1)[1]

    shop_page.open_store()
    product_page = ProductPage(driver)
    product_page.load(product_id)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "custom-rating")))

    # Step 5: Get previous rating and count
    old_rating = product_page.get_average_rating()
    old_count = product_page.get_review_count()

    # Step 6: Remove existing review if any
    product_page.remove_existing_review()

    # Step 6.1: Wait for the form to reappear after deletion
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "interactive-rating")))
    except:
        raise Exception("Review form did not reappear after deleting existing review.")

    # Step 6.2: Submit review with a randomized star rating
    rating = random.randint(1, 5)
    product_page.select_star_rating(rating)
    product_page.submit_review()

    # Step 7: Wait for the new rating to appear
    time.sleep(2)
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "custom-rating")))

    # Step 8: Fetch all actual review ratings
    actual_average = product_page.get_average_from_visible_reviews()

    # Step 9: Compare to displayed value
    displayed_avg = product_page.get_average_rating()

    # Step 10: Assert
    assert math.isclose(actual_average, displayed_avg, abs_tol=0.11), \
        f"Displayed average ({displayed_avg}) does not match actual average ({actual_average})"

    # Step 11: Confirm the count increased
    new_count = product_page.get_review_count()
    assert new_count == old_count, (
        f"Review count changed unexpectedly. Before: {old_count}, After: {new_count}"
    )
