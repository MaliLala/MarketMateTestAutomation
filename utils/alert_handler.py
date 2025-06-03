from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def accept_alert(driver, timeout=5):
    """
    Wait for a JavaScript alert to appear and accept it.

    Args:
        driver: Selenium WebDriver instance
        timeout: Max wait time for the alert
    """
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except Exception as e:
        print("⚠️ Alert not accepted:", str(e))
