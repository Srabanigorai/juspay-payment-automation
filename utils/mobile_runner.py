"""Appium helpers: driver creation, locator parsing, declarative step execution."""
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import APPIUM_URL, DEFAULT_TIMEOUT_MS

_BY = {
    "id": AppiumBy.ID,
    "acc": AppiumBy.ACCESSIBILITY_ID,
    "xpath": AppiumBy.XPATH,
    "uia": AppiumBy.ANDROID_UIAUTOMATOR,
}


def parse_locator(spec: str):
    kind, _, value = spec.partition("=")
    if kind not in _BY:
        raise ValueError(f"Locator must start with one of {list(_BY)}: {spec}")
    return _BY[kind], value


def create_driver(target: dict, udid: str | None = None):
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.automation_name = "UiAutomator2"
    opts.app_package = target["app_package"]
    opts.app_activity = target["app_activity"]
    opts.no_reset = True
    opts.new_command_timeout = 300
    if udid:
        opts.udid = udid
    return webdriver.Remote(APPIUM_URL, options=opts)


def _wait(driver, locator: str, clickable=False):
    by, value = parse_locator(locator)
    cond = EC.element_to_be_clickable if clickable else EC.visibility_of_element_located
    return WebDriverWait(driver, DEFAULT_TIMEOUT_MS / 1000).until(cond((by, value)))


def run_steps(driver, steps: list[dict]):
    for i, s in enumerate(steps, 1):
        a = s["action"]
        print(f"  step {i}: {s.get('note', a + ' ' + str(s.get('locator', '')))}")
        if a == "click":
            _wait(driver, s["locator"], clickable=True).click()
        elif a == "fill":
            el = _wait(driver, s["locator"])
            el.click()
            el.clear()
            el.send_keys(s["value"])
        elif a == "wait_for":
            _wait(driver, s["locator"])
        elif a == "pause":
            driver.implicitly_wait(0)
            import time; time.sleep(int(s["value"]) / 1000)
        elif a == "back":
            driver.back()
        elif a == "scroll_to_text":
            driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().textContains("{s["value"]}"))')
        else:
            raise ValueError(f"Unknown action: {a}")
