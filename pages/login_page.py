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

    def login(self, email: str, password: str) -> None:
        """
        Navigate to the auth page, enter credentials, and submit.

        Args:
            email: Email address to log in with.
            password: User's password.
        """
        self._driver.get(self._PAGE_URL)

        email_el = self._wait.until(
            EC.element_to_be_clickable(self._EMAIL_INPUT)
        )
        email_el.clear()
        email_el.send_keys(email)

        pwd_el = self._wait.until(
            EC.element_to_be_clickable(self._PASSWORD_INPUT)
        )
        pwd_el.clear()
        pwd_el.send_keys(password)

        self._wait.until(
            EC.element_to_be_clickable(self._SUBMIT_BUTTON)
        ).click()
