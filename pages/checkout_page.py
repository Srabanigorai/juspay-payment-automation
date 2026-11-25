
from playwright.sync_api import Page, expect


class CheckoutPage:
    """Cart and payment-method screens of the mock checkout."""

    def __init__(self, page: Page):
        self.page = page

    def open(self, base_url: str):
        self.page.goto(base_url)

        expect(
            self.page.get_by_role("heading", name="Your cart")
        ).to_be_visible()

    def proceed_to_pay(self):
        self.page.get_by_role(
            "button", name="Proceed to pay"
        ).click()

        expect(
            self.page.get_by_role(
                "heading", name="Choose payment method"
            )
        ).to_be_visible()

    def select_method(self, name: str):
        tab = self.page.get_by_role("tab", name=name)
        tab.click()

        expect(tab).to_have_attribute(
            "aria-selected", "true"
        )

    def pay_by_card(self, card: dict):
        self.select_method("Card")

        frame = self.page.frame_locator("#card-frame")

        frame.get_by_label("Card number").fill(card["number"])
        frame.get_by_label("Expiry (MM/YY)").fill(card["expiry"])
        frame.get_by_label("CVV").fill(card["cvv"])
        frame.get_by_label("Name on card").fill(card["name"])

        frame.get_by_role("button", name="Pay").click()

    def card_error(self):
        return self.page.frame_locator(
            "#card-frame"
        ).get_by_role("alert")

    def pay_by_upi(self, upi_id: str):
        self.select_method("UPI")

        self.page.get_by_label("UPI ID").fill(upi_id)

        self.page.get_by_role(
            "button", name="Verify and pay"
        ).click()

    def pay_by_netbanking(self, bank: str):
        self.select_method("Netbanking")

        self.page.get_by_label(
            "Select bank"
        ).select_option(bank)

        self.page.get_by_role(
            "button", name="Pay via netbanking"
        ).click()
