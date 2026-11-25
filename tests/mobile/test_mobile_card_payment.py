import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, load_card


@pytest.mark.mobile
def test_mobile_card_payment_reaches_second_factor(driver):
    """Mobile-web flow in Chrome on an Android emulator.
    Adjust locators via chrome://inspect if the demo page changes."""
    wait = WebDriverWait(driver, 40)
    driver.get(BASE_URL)

    wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH,
        "//button[contains(translate(.,'CHECKOUTPAYBUY','checkoutpaybuy'),'checkout') or "
        "contains(translate(.,'PAYBUY','paybuy'),'pay') or "
        "contains(translate(.,'BUY','buy'),'buy')]"))).click()

    card = load_card("success_3ds")
    wait.until(EC.presence_of_element_located((AppiumBy.CSS_SELECTOR, "#cardNumber"))).send_keys(card["number"])
    driver.find_element(AppiumBy.CSS_SELECTOR, "#cardExpiry").send_keys(card["expiry"].replace("/", ""))
    driver.find_element(AppiumBy.CSS_SELECTOR, "#cardCvc").send_keys(card["cvc"])
    driver.find_element(AppiumBy.CSS_SELECTOR, "#billingName").send_keys(card["name"])
    driver.find_element(AppiumBy.CSS_SELECTOR, "button[type='submit']").click()

    # 3DS challenge renders in an iframe; its presence = second factor reached
    wait.until(EC.presence_of_element_located((AppiumBy.CSS_SELECTOR, "iframe")))
