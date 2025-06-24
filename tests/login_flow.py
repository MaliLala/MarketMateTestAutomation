import pytest
from pages.login_page import LoginPage

@pytest.mark.usefixtures("driver", "config")
def test_login(driver, config):
    """
    Execute login flow:

    1. Open homepage.
    2. Click login icon.
    3. Enter credentials.
    4. Submit.
    """
    LoginPage(driver).login(
        email=config["email"],
        password=config["password"],
    )
