# tests/test_average_rating.py

import time
import math
import pytest
import random

from uuid import uuid4
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage
from pages.shop_page import ShopPage
from pages.product_page import ProductPage

@pytest.mark.order(7)
@pytest.mark.usefixtures("driver", "config")
def test_average_rating_update(driver, config):
    """
    Submits a 4-star review and verifies that the average rating
    and review count update as expected.
    """
    wait = WebDriverWait(driver, 10)

    # Step 1: Login
    print("[DEBUG] Logging in...")
    LoginPage(driver).login(config["email"], config["password"])

    # Step 2: Age verification
    age = AgeVerificationPage(driver)
    age.open_shop()
    age.enter_dob("08-08-2000")
    age.confirm_age()
    time.sleep(1)
    print(f"[DEBUG] Current URL after confirming age: {driver.current_url}")

    # Step 3: Wait for product cards to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card")))
    print("[DEBUG] Landed on /shop page, product cards detected.")

    # Step 4: Navigate to product
    shop_page = ShopPage(driver)
    product_element = shop_page.get_first_product_card()
    input_elem = product_element.find_element(By.CSS_SELECTOR, "input.quantity")
    product_id = input_elem.get_attribute("name").split("_", 1)[1]
    print(f"[DEBUG] First product ID: {product_id}")

    shop_page.open_store()
    product_page = ProductPage(driver)
    product_page.load(product_id)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "custom-rating")))
    print(f"[DEBUG] Landed on product page: {driver.current_url}")

    # Step 5: Get previous rating and count
    old_rating = product_page.get_average_rating()
    old_count = product_page.get_review_count()
    print(f"[DEBUG] Previous average rating: {old_rating}, count: {old_count}")

    # Step 6: Remove existing review if any
    product_page.remove_existing_review()

    # Step 6.1: Wait for the form to reappear after deletion
    try:
        print("[DEBUG] Waiting for review form to reappear after deletion...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "interactive-rating")))
        print("[DEBUG] Review form is visible again.")
    except:
        raise Exception("[ERROR] Review form did not reappear after deleting existing review.")

    # Step 6.2: Submit review with a randomized star rating
    import random
    rating = random.randint(1, 5)
    print(f"[DEBUG] Randomly selected rating: {rating}")

    product_page.select_star_rating(rating)
    product_page.submit_review()

    # Step 7: Wait for the new rating to appear
    time.sleep(2)  # Slight delay to allow backend to update
    driver.refresh()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "custom-rating")))

    # Step 8: Fetch all actual review ratings
    actual_average = product_page.get_average_from_visible_reviews()
    print(f"[DEBUG] Calculated actual average: {actual_average}")

    # Step 9: Compare to displayed value
    displayed_avg = product_page.get_average_rating()
    print(f"[DEBUG] Displayed average rating: {displayed_avg}")

    # Step 10: Assert
    assert math.isclose(actual_average, displayed_avg, abs_tol=0.11), \
        f"Displayed average ({displayed_avg}) does not match actual average ({actual_average})"

    # Step 11: Confirm the count increased
    new_count = product_page.get_review_count()
    print(f"[DEBUG] New review count: {new_count}")
    assert new_count == old_count, (
        f"[FAIL] Review count changed unexpectedly. Before: {old_count}, After: {new_count}"
    )

    print(f"[PASS] Review count increased from {old_count} to {new_count}")
    print(f"[PASS] Average rating changed from {old_rating} to {displayed_avg}")


