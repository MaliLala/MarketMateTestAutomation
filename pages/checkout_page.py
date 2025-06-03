# pages/checkout_page.py

import time  # For adding delays during UI interactions
from selenium.webdriver.common.by import By  # Used to locate elements
from selenium.webdriver.support.ui import WebDriverWait  # Waits for conditions
from selenium.webdriver.support import expected_conditions as EC  # Common wait conditions


class CheckoutPage:
    """Handles checkout flow: shipping-cost reads, quantity adjustments, and full purchases."""

    # — existing shipping-cost locators & actions —
    _CHECKOUT_URL = "https://grocerymate.masterschool.com/checkout"  # URL for the checkout page
    _SHIPPING_COST = (
        By.XPATH,
        "//h5[normalize-space(.)='Shipment:']/following-sibling::h5"
    )  # Finds the element with shipping cost
    _PLUS_BUTTON = (By.CSS_SELECTOR, "button.plus")  # Locator for increasing quantity
    _MINUS_BUTTON = (By.CSS_SELECTOR, "button.minus")  # Locator for decreasing quantity

    # — updated locators for the “buy” flow —
    _STREET = (By.NAME, "street")  # Input field for street
    _CITY = (By.NAME, "city")  # Input field for city
    _POSTAL_CODE = (By.NAME, "postalCode")  # Input for ZIP code
    _CARD_NUMBER = (By.NAME, "cardNumber")  # Credit card number input
    _NAME_ON_CARD = (By.NAME, "nameOnCard")  # Name on card input
    _EXPIRATION = (By.NAME, "expiration")  # Expiry date input
    _CVV = (By.NAME, "cvv")  # CVV code input
    _CONTINUE = (By.XPATH, "//button[contains(text(),'Buy now')]")  # Final purchase button


    def __init__(self, driver, timeout: int = 15):
        self.driver = driver  # Store reference to Selenium driver
        self.wait = WebDriverWait(driver, timeout)  # Create WebDriverWait with timeout

    # — shipping-cost & quantity methods —
    def open_checkout(self):
        """Navigate directly to the checkout page and wait for React to render."""
        self.driver.get(self._CHECKOUT_URL)  # Go to checkout URL
        self.wait.until(EC.url_contains("/checkout"))  # Wait until URL confirms we’re there
        time.sleep(1)  # Allow hydration/render time for React

    def read_shipping_cost(self) -> str:
        """Wait for and return the visible shipping-cost text."""
        el = self.wait.until(EC.visibility_of_element_located(self._SHIPPING_COST))  # Wait for cost to show
        return el.text.strip()  # Return cleaned text

    def increase_quantity(self, times: int = 1):
        """Click the '+' button `times` times, with a pause after each."""
        btn = self.wait.until(EC.element_to_be_clickable(self._PLUS_BUTTON))  # Wait until plus button is clickable
        for _ in range(times):  # Repeat clicking
            btn.click()
            time.sleep(0.5)  # Small delay to let UI update

    def decrease_quantity(self, times: int = 1):
        """Click the '–' button `times` times, with a pause after each."""
        btn = self.wait.until(EC.element_to_be_clickable(self._MINUS_BUTTON))  # Wait until minus button is clickable
        for _ in range(times):  # Repeat clicking
            btn.click()
            time.sleep(0.5)  # Delay between actions

    # — purchase (“buy”) methods —
    def fill_checkout_form(
        self,
        first: str = "Test",
        last: str = "User",
        address: str = "123 Test St",
        city: str = "Testville",
        zip_code: str = "10001",
    ) -> None:
        """Fill the checkout form and place the order."""
        self.wait.until(EC.presence_of_element_located(self._STREET)).send_keys(address)  # Fill street
        self.wait.until(EC.presence_of_element_located(self._CITY)).send_keys(city)  # Fill city
        self.wait.until(EC.presence_of_element_located(self._POSTAL_CODE)).send_keys(zip_code)  # Fill ZIP
        self.wait.until(EC.presence_of_element_located(self._CARD_NUMBER)).send_keys("4111111111111111")  # Dummy card
        self.wait.until(EC.presence_of_element_located(self._NAME_ON_CARD)).send_keys(f"{first} {last}")  # Name
        self.wait.until(EC.presence_of_element_located(self._EXPIRATION)).send_keys("12/2029")  # Expiry date
        self.wait.until(EC.presence_of_element_located(self._CVV)).send_keys("123")  # CVV code
        self.driver.find_element(*self._CONTINUE).click()  # Click "Buy now"

    def wait_for_order_confirmation(self):
        """Wait until the app redirects to homepage (used as order confirmation)."""
        self.wait.until(EC.url_to_be("https://grocerymate.masterschool.com/"))  # Wait for homepage load

    def buy(
        self,
        first: str = "Test",
        last: str = "User",
        address: str = "123 Test St",
        city: str = "Testville",
        zip_code: str = "10001",
    ):
        """
        Full purchase helper: open checkout, fill the form, place order,
        and wait for confirmation. Does not affect existing shipping tests.
        """
        self.open_checkout()  # Open checkout page
        self.fill_checkout_form(  # Fill form with given values
            first=first,
            last=last,
            address=address,
            city=city,
            zip_code=zip_code,
        )
        self.wait_for_order_confirmation()  # Wait for homepage

    def place_order(self):
        """
        Clicks the 'Buy now' or final submission button to place the order.
        """
        self.wait.until(EC.element_to_be_clickable(self._CONTINUE)).click()

    def clear_cart(self):
        """Remove all items from the cart by clicking their × icons."""
        self.open_checkout()  # Ensure we are on checkout page

        while True:
            try:
                remove_buttons = self._driver.find_elements(By.XPATH, "//button[contains(text(),'×')]")  # Find all remove buttons
                if not remove_buttons:
                    break  # Nothing left to remove

                for btn in remove_buttons:  # For each remove button
                    self.wait.until(EC.element_to_be_clickable(btn)).click()  # Wait then click
                    time.sleep(0.5)  # Allow UI to update
            except Exception:
                break  # If interaction fails, stop
