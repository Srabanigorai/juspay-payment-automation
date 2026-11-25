import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    page.goto("https://demo.pxp.io/dropin")
    page.get_by_role("button", name="plus Cart").nth(2).click()
    page.get_by_role("link", name="shopping-cart").click()
    page.get_by_role("button", name="arrow-right Proceed to").click()
    page.get_by_label("Payment method Card").click()
    page.locator("#card-number-1795596463231-3laa2ju iframe").content_frame.locator("#shadow-root-container").click()
    page.locator("#card-number-1795596463231-3laa2ju iframe").content_frame.locator("#shadow-root-container").click()
    page.locator("#card-expiry-date-1795596463232-aids6to iframe").content_frame.locator("#shadow-root-container").click()
    page.locator("#card-cvc-1795596463231-tmck3pc iframe").content_frame.locator("#shadow-root-container").click()
    page.locator("#card-holder-name-1795596463233-kxnmsn6 iframe").content_frame.locator("#shadow-root-container").click()
    page.get_by_role("textbox", name="Select country").click()
    page.get_by_role("textbox", name="Select country").fill("India")
    page.get_by_text("India").nth(1).click()
    page.get_by_role("textbox", name="Postcode").click()
    page.get_by_role("textbox", name="Postcode").fill("110001")
    page.get_by_role("textbox", name="Example Street, City").click()
    page.get_by_role("textbox", name="Example Street, City").fill("Test Street 123,New Delhi")
    page.locator("#card-submit-1795596463235-8kyh20d-button").click()
    page.locator("#unity-3ds-challenge-4d81171e-bba0-42b5-bea0-4614e22de337").content_frame.get_by_role("button", name="Approve").click()
    page.goto("https://demo.pxp.io/dropin/thank-you")
    page.get_by_role("button", name="home Continue shopping").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
