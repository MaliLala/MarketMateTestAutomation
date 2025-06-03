import pytest
from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage


@pytest.mark.order(1)
@pytest.mark.usefixtures("driver", "config")
class TestValidDOB:
    """Test case: Valid DOB allows access to restricted products."""

    def test_valid_dob_shows_success(self, driver, config):
        LoginPage(driver).login(config["email"], config["password"])
        driver.get("https://grocerymate.masterschool.com")

        page = AgeVerificationPage(driver)
        page.open_shop()
        page.enter_dob("08-08-2000")  # Valid DOB (18+)
        page.confirm_age()

        msg = page.get_toast_message().lower()
        assert "you are of age" in msg
