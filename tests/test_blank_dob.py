import pytest
from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage


@pytest.mark.order(2)
@pytest.mark.usefixtures("driver", "config")
class TestBlankDOB:
    """Test case: Blank DOB shows error message and blocks access."""

    def test_blank_dob_shows_prompt(self, driver, config):
        LoginPage(driver).login(config["email"], config["password"])
        driver.get("https://grocerymate.masterschool.com")

        page = AgeVerificationPage(driver)
        page.open_shop()
        page.enter_dob("")  # Blank input
        page.confirm_age()

        msg = page.get_toast_message().lower()
        assert "you are underage" in msg or "please enter your birth date" in msg
