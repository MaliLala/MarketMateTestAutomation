import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutCleaner:
    """
    Utility class to remove all items from the cart on the checkout page.
    """

    _CHECKOUT_URL = "https://grocerymate.masterschool.com/checkout"
    _REMOVE_LINKS = (By.CSS_SELECTOR, "a.remove-icon")  # Fix: <a> tag, not button
    _CART_EMPTY_INDICATOR = (By.CLASS_NAME, "cart-empty-text")  # Optional final check

    def __init__(self, driver):
        """
        Initialize with the Selenium WebDriver instance.

        Args:
            driver: Selenium WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def clear_cart(self):
        """
        Clicks all '×' icons in the checkout to remove items from the cart.
        """
        self.driver.get(self._CHECKOUT_URL)
        self.wait.until(EC.presence_of_element_located(self._REMOVE_LINKS))
        time.sleep(2)  # Let cart render fully

        while True:
            remove_buttons = self.driver.find_elements(*self._REMOVE_LINKS)
            # Filter only those that actually contain the "×" character
            x_buttons = [btn for btn in remove_buttons if btn.text.strip() == "×"]

            if not x_buttons:
                print("✅ Cart is empty.")
                break

            for button in x_buttons:
                try:
                    self.wait.until(EC.element_to_be_clickable(button))
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    button.click()
                    time.sleep(2)  # Let cart update
                    break  # Re-evaluate DOM after each removal
                except Exception as e:
                    print(f"❌ Failed to click '×': {e}")
                    continue
