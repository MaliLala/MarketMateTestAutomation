import pytest

from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage


@pytest.mark.order(10)
@pytest.mark.usefixtures("driver", "config")
class TestUnderageBlock:
    """Verify that underage users are blocked from accessing restricted products."""

    def test_underage_dob_shows_block_message(self, driver, config):
        # Log in
        LoginPage(driver).login(config["email"], config["password"])

        # Navigate to age gate
        driver.get("https://grocerymate.masterschool.com")
        page = AgeVerificationPage(driver)
        page.open_shop()

        # Enter an underage DOB
        page.enter_dob("08-08-2008")
        page.confirm_age()

        # Expect appropriate toast message
        msg = page.get_toast_message().lower()
        assert "you are underage" in msg
