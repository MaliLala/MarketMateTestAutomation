from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    """Page object for login via the /auth page."""

    _PAGE_URL = "https://grocerymate.masterschool.com/auth"
    _EMAIL_INPUT = (By.XPATH, '//input[@placeholder="Email address"]')
    _PASSWORD_INPUT = (By.XPATH, '//input[@placeholder="Password"]')
    _SUBMIT_BUTTON = (By.CLASS_NAME, "submit-btn")

    def __init__(self, driver):
        """
        Initialize with a WebDriver and default wait.

        Args:
            driver: Selenium WebDriver instance.
        """
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def load(self):
        """Navigate to the login page URL."""
        self._driver.get(self._PAGE_URL)

    def login(self, email: str, password: str) -> None:
        self._driver.get(self._PAGE_URL)

        email_el = self._wait.until(EC.element_to_be_clickable(self._EMAIL_INPUT))
        email_el.clear()
        email_el.send_keys(email)

        pwd_el = self._wait.until(EC.element_to_be_clickable(self._PASSWORD_INPUT))
        pwd_el.clear()
        pwd_el.send_keys(password)

        self._wait.until(EC.element_to_be_clickable(self._SUBMIT_BUTTON)).click()

        # Wait until the URL changes to the home page (login success confirmation)
        self._wait.until(EC.url_to_be("https://grocerymate.masterschool.com/"))




