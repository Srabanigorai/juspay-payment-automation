"""Selector-driven journeys against real sites listed in config/targets.yaml.

Each enabled target must reach its second-factor page. If the target also defines
otp_value + submit_selector + success_selector (sandbox/test-mode only), the
transaction is completed as well.
"""
import pytest
from playwright.sync_api import expect

from config.settings import DEFAULT_TIMEOUT_MS
from utils.data import load_targets
from utils.step_runner import run_steps

TARGETS = load_targets("targets.yaml")

pytestmark = pytest.mark.live


@pytest.mark.skipif(not TARGETS, reason="No live target enabled in config/targets.yaml")
@pytest.mark.parametrize("target", TARGETS, ids=[t["name"] for t in TARGETS])
def test_live_flow_reaches_second_factor(page, target):
    page.set_default_timeout(DEFAULT_TIMEOUT_MS)
    run_steps(page, target["steps"])
    otp = page.locator(target["otp_selector"]).first
    expect(otp).to_be_visible(timeout=30000)
    page.screenshot(path=f"reports/{target['name']}-second-factor.png")

    if target.get("otp_value"):  # bonus: complete the transaction (sandbox only)
        otp.fill(target["otp_value"])
        page.locator(target["submit_selector"]).first.click()
        expect(page.locator(target["success_selector"]).first).to_be_visible(timeout=30000)
