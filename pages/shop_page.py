import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ShopPage:
    _STORE_URL = "https://grocerymate.masterschool.com/store"

    # Age verification modal locators exactly as before
    _SHOP_BUTTON = (By.XPATH, '//a[@href="/store"]')
    _DOB_INPUT = (By.XPATH, "//div[contains(@class, 'modal-content')]//input[@placeholder='DD-MM-YYYY']")
    _CONFIRM_BUTTON = (By.XPATH, '//button[contains(text(), "Confirm")]')
    _TOAST = (By.XPATH, "//div[contains(text(), 'You are of age')"
                        " or contains(text(), 'You are underage')"
                        " or contains(text(), 'Please enter your birth date')]")

    def __init__(self, driver):
        """
        Initialize with WebDriver and setup waits.
        """
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)
        self._toast_wait = WebDriverWait(driver, 15, poll_frequency=0.5)

    def load(self):
        """Navigate to the store page URL."""
        self._driver.get(self._STORE_URL)

    def open_store(self):
        """
        Navigate directly to the store page URL and wait for
        either product cards or the DOB modal to appear.
        """
        self._driver.get(self._STORE_URL)
        self._wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.CLASS_NAME, "product-card")),
                EC.presence_of_element_located(self._DOB_INPUT),
            )
        )

    def open_shop_modal(self):
        """
        Click the SHOP link that triggers the age verification modal,
        and wait for the DOB input field to appear.
        """
        shop_button = self._wait.until(
            EC.element_to_be_clickable(self._SHOP_BUTTON)
        )
        shop_button.click()
        self._wait.until(EC.visibility_of_element_located(self._DOB_INPUT))

    def handle_age_verification(self, dob: str):
        """
        Enter DOB into modal and confirm.
        """
        dob_input = self._wait.until(
            EC.visibility_of_element_located(self._DOB_INPUT)
        )
        dob_input.clear()
        dob_input.send_keys(dob)

        confirm_button = self._wait.until(
            EC.element_to_be_clickable(self._CONFIRM_BUTTON)
        )
        confirm_button.click()

        time.sleep(1)  # Allow UI to react after confirmation

    def get_toast_message(self) -> str:
        """
        Wait for any of the expected toasts and return its text.
        """
        return self._toast_wait.until(
            EC.presence_of_element_located(self._TOAST)
        ).text

    def toast_message_displayed(self, expected_text: str) -> bool:
        """
        Check if a toast with expected text is visible.
        """
        try:
            toast = self._toast_wait.until(
                EC.visibility_of_element_located(self._TOAST)
            )
            return expected_text.lower() in toast.text.lower()
        except Exception:
            return False

    def get_first_product_card(self):
        """
        Return the first product card element on the store page.
        """
        self._wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card"))
        )
        card = self._driver.find_elements(By.CLASS_NAME, "product-card")[0]
        self._driver.execute_script("arguments[0].scrollIntoView(true);", card)
        time.sleep(0.3)
        return card

    def get_first_product_price(self) -> float:
        """
        Returns the price of the first product card as a float.
        Used in shipping cost tests to determine quantity to exceed threshold.
        """
        card = self.get_first_product_card()
        price_text = None

        for class_name in ["discount-price", "price"]:
            try:
                price_text = card.find_element(By.CLASS_NAME, class_name).text
                break
            except Exception:
                continue

        if not price_text:
            try:
                price_elem = card.find_element(By.XPATH, ".//*[contains(text(),'€')]")
                price_text = price_elem.text
            except Exception:
                raise Exception("Could not locate price element in product card")

        return float(price_text.replace("€", "").strip().replace(",", "."))

    def add_first_product_to_cart(self, quantity: int = 1):
        """Add the first product on the page to the cart with specified quantity."""
        card = self.get_first_product_card()

        qty_input = card.find_element(By.XPATH, ".//input[contains(@class, 'quantity')]")
        add_btn = card.find_element(By.CSS_SELECTOR, "button.btn-cart")

        self._driver.execute_script("arguments[0].scrollIntoView(true);", qty_input)
        qty_input.clear()
        qty_input.send_keys(str(quantity))
        time.sleep(0.5)

        self._driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
        add_btn.click()
