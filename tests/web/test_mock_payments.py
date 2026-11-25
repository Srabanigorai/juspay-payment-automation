"""Multi-method payment journeys on the bundled mock checkout.

Reaches the OTP (second-factor) page for card, UPI and netbanking, and completes
successful transactions by entering the fixed sandbox OTP.
"""
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.mock


# ---- Reach the second-factor page -------------------------------------------------
def test_card_reaches_otp(checkout, otp, data):
    checkout.pay_by_card(data["success"])
    otp.expect_visible()


def test_upi_reaches_otp(checkout, otp, data):
    checkout.pay_by_upi(data["upi_id"])
    otp.expect_visible()


def test_netbanking_reaches_otp(checkout, otp, data):
    checkout.pay_by_netbanking(data["bank"])
    otp.expect_visible()


# ---- Bonus: complete the transaction with the OTP ---------------------------------
def test_card_successful_transaction(checkout, otp, data):
    checkout.pay_by_card(data["success"])
    otp.expect_visible()
    otp.submit(data["otp_valid"])
    otp.expect_success()


def test_upi_successful_transaction(checkout, otp, data):
    checkout.pay_by_upi(data["upi_id"])
    otp.submit(data["otp_valid"])
    otp.expect_success()


def test_netbanking_successful_transaction(checkout, otp, data):
    checkout.pay_by_netbanking(data["bank"])
    otp.submit(data["otp_valid"])
    otp.expect_success()


# ---- Negative paths ---------------------------------------------------------------
def test_wrong_otp_then_correct_otp(checkout, otp, data):
    checkout.pay_by_card(data["success"])
    otp.submit(data["otp_invalid"])
    expect(otp.error()).to_contain_text("Invalid OTP")
    otp.submit(data["otp_valid"])
    otp.expect_success()


def test_three_wrong_otps_fail_payment(checkout, otp, data, page):
    checkout.pay_by_card(data["success"])
    for _ in range(3):
        otp.submit(data["otp_invalid"])
    expect(page.get_by_role("heading", name="Payment failed")).to_be_visible()


def test_declined_card_never_reaches_otp(checkout, data, page):
    checkout.pay_by_card(data["declined"])
    expect(checkout.card_error()).to_have_text("Card declined by issuer")
    expect(page.get_by_role("heading", name="Enter OTP")).to_be_hidden()


def test_invalid_card_number_rejected(checkout, data):
    checkout.pay_by_card(data["invalid"])
    expect(checkout.card_error()).to_have_text("Invalid card number")
