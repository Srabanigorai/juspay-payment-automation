from playwright.sync_api import Page, expect


class OtpPage:
    """Second-factor screen and the final result screens."""

    def __init__(self, page: Page):
        self.page = page

    def expect_visible(self):
        expect(self.page.get_by_role("heading", name="Enter OTP")).to_be_visible()
        expect(self.page.get_by_label("One-time password")).to_be_visible()

    def submit(self, otp: str):
        self.page.get_by_label("One-time password").fill(otp)
        self.page.get_by_role("button", name="Submit OTP").click()

    def error(self):
        return self.page.locator("#otp-error")

    def expect_success(self):
        expect(self.page.get_by_role("heading", name="Payment successful")).to_be_visible()
        expect(self.page.locator("#txn-id")).to_contain_text("TXN")
