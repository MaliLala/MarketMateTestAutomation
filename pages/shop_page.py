import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ShopPage:
    _STORE_URL = "https://grocerymate.masterschool.com/store"

    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def open_store(self):
        """Open the store page and wait for product cards to load."""
        self._driver.get(self._STORE_URL)
        self._wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card")))

    def get_first_product_card(self):
        """
        Returns the WebElement of the first product card on the store page.
        Used by review tests to click into the product page.
        """
        self._wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card")))
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
        """
        Add the first product on the page to the cart with specified quantity.
        Used in shipping cost test and other cart-related tests.
        """
        card = self.get_first_product_card()

        qty_input = card.find_element(By.XPATH, ".//input[@type='number']")
        add_btn = card.find_element(By.XPATH, ".//button[contains(text(),'Add to Cart')]")

        self._driver.execute_script("arguments[0].scrollIntoView(true);", qty_input)
        qty_input.clear()
        qty_input.send_keys(str(quantity))
        time.sleep(0.5)

        self._driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
        add_btn.click()
