# conftest.py

import configparser
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


@pytest.fixture(scope="session")
def config() -> configparser.SectionProxy:
    """
    Read configuration (e.g. auth credentials) from config.ini.
    Expects a [auth] section with 'email' and 'password'.
    """
    parser = configparser.ConfigParser()
    parser.read("config.ini")
    return parser["auth"]


@pytest.fixture(scope="function")
def driver() -> webdriver.Chrome:
    """
    Function-scoped WebDriver: a fresh Chrome instance for each test function.
    """
    options = Options()
    options.add_argument("--start-maximized")
    driver_instance = webdriver.Chrome(options=options)
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(autouse=True)
def clear_browser_state(driver):
    """
    Before each test using `driver`:
      - Delete all cookies
      - Attempt to clear localStorage if on a real page
    """
    driver.delete_all_cookies()

    try:
        driver.execute_script("window.localStorage.clear();")
    except WebDriverException:
        # e.g. on about:blank or data: URLs
        pass

    yield


@pytest.fixture(scope="class")
def class_driver() -> webdriver.Chrome:
    """
    Class-scoped WebDriver: one Chrome instance shared by all methods
    in any TestClass that requests this fixture.
    """
    options = Options()
    options.add_argument("--start-maximized")
    driver_instance = webdriver.Chrome(options=options)
    yield driver_instance
    driver_instance.quit()
