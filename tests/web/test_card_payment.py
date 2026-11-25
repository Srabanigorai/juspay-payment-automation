import pytest

from config.settings import BASE_URL, START_SELECTOR, load_card
from pages.checkout_page import CheckoutPage
from pages.otp_page import OtpPage


def _pay(page, card_name):
    checkout = CheckoutPage(page)
    checkout.open(BASE_URL)
    checkout.start_checkout(START_SELECTOR)
    checkout.pay_with_card(load_card(card_name))
    return checkout


@pytest.mark.web
def test_card_payment_reaches_second_factor(page):
    """Core deliverable: card payment up to the 3DS / OTP page."""
    _pay(page, "success_3ds")
    assert OtpPage(page).wait_for_second_factor()


@pytest.mark.web
@pytest.mark.otp
def test_card_payment_completes_3ds_successfully(page):
    """Bonus: finish the sandbox challenge and leave the hosted checkout (success redirect)."""
    checkout = _pay(page, "success_3ds")
    otp = OtpPage(page)
    otp.wait_for_second_factor()
    otp.complete_authentication()
    page.wait_for_url(lambda url: "checkout.stripe.com" not in url, timeout=45_000)
    checkout.screenshot("payment_success")


@pytest.mark.web
def test_card_payment_without_3ds(page):
    """Variant: card with no 3DS challenge goes straight to success."""
    _pay(page, "success_no_3ds")
    page.wait_for_url(lambda url: "checkout.stripe.com" not in url, timeout=45_000)
