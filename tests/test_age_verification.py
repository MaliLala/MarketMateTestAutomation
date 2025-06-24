import pytest
from pages.login_page import LoginPage
from pages.shop_page import ShopPage


@pytest.mark.usefixtures("driver", "config")
class TestAgeVerification:

    def test_blank_dob_shows_prompt(self, driver, config):
        """
        Submitting a blank DOB should trigger a toast and block access.
        """
        login = LoginPage(driver)
        login.load()
        login.login(config["email"], config["password"])

        shop = ShopPage(driver)
        shop.load()
        shop.handle_age_verification("")

        assert shop.toast_message_displayed("underage") or shop.toast_message_displayed("birth")

    def test_underage_dob_shows_block_message(self, driver, config):
        """
        Entering an underage DOB should block access and show a toast.
        """
        login = LoginPage(driver)
        login.load()
        login.login(config["email"], config["password"])

        shop = ShopPage(driver)
        shop.load()
        shop.handle_age_verification("08-08-2008")

        assert shop.toast_message_displayed("underage")

    def test_valid_dob_grants_access(self, driver, config):
        """
        A valid DOB (18+) should allow access without any error toasts.
        """
        login = LoginPage(driver)
        login.load()
        login.login(config["email"], config["password"])

        shop = ShopPage(driver)
        shop.load()
        shop.handle_age_verification("08-08-2000")

        assert not shop.toast_message_displayed("underage")
        assert not shop.toast_message_displayed("birth")
