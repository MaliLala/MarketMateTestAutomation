import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AgeVerificationPage:
    """Page object for age-verification via the SHOP link and toast messages."""

    # Locator for the SHOP link that opens the DOB popup
    _SHOP_BUTTON = (
        By.XPATH,
        '/html/body/div/div/div[2]/div/div/ul/li[2]/a'
    )

    # Locator for the DOB input field
    _DOB_INPUT = (
        By.XPATH,
        '/html/body/div/div/div[3]/div[2]/div/div[2]/div/input'
    )

    # Locator for the Confirm button in age popup
    _CONFIRM_BUTTON = (
        By.XPATH,
        '//button[contains(text(), "Confirm")]'
    )

    # Generic toast locator for all possible messages
    _TOAST = (
        By.XPATH,
        "//div[contains(text(), 'You are of age')"
        " or contains(text(), 'You are underage')"
        " or contains(text(), 'Please enter your birth date')]"
    )

    def __init__(self, driver):
        """
        Initialize with a WebDriver and set up waits.

        Args:
            driver: Selenium WebDriver instance.
        """
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)  # Standard short wait
        self._toast_wait = WebDriverWait(driver, 15, poll_frequency=0.5)  # Longer wait for toast

    def open_shop(self) -> None:
        """Click SHOP to open the age-verification popup."""
        self._wait.until(
            EC.element_to_be_clickable(self._SHOP_BUTTON)  # 🔴
        ).click()

    def enter_dob(self, dob: str) -> None:
        """
        Enter the date of birth.

        Args:
            dob: 'DD-MM-YYYY' or '' for blank.
        """
        # Wait for the DOB input to be visible 🔴
        dob_el = self._wait.until(
            EC.visibility_of_element_located(self._DOB_INPUT)
        )
        dob_el.clear()  # Clear any prefilled data
        dob_el.send_keys(dob)  # Enter provided DOB

    def confirm_age(self) -> None:
        """Click Confirm and give the page time to render the toast."""
        self._wait.until(
            EC.element_to_be_clickable(self._CONFIRM_BUTTON)  # 🔴
        ).click()
        time.sleep(1)  # Small wait to let the UI react (React hydration)

    def get_toast_message(self) -> str:
        """
        Wait for any of the expected toasts and return its text.

        Returns:
            The toast message text.
        """
        return self._toast_wait.until(  # Wait up to 15s for any matching toast
            EC.presence_of_element_located(self._TOAST)  # 🔴
        ).text
