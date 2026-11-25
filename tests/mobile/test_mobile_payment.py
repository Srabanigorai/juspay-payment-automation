"""Android payment journey through Appium; stops at the second-factor screen.

Records the device screen to reports/videos/<target>.mp4.
"""
import base64
import os
import socket
from urllib.parse import urlparse

import pytest

from config.settings import APPIUM_URL, REPORTS
from utils.data import load_targets
from utils.mobile_runner import create_driver, run_steps, _wait

TARGETS = load_targets("mobile_targets.yaml")

pytestmark = pytest.mark.mobile


def _appium_up() -> bool:
    u = urlparse(APPIUM_URL)
    try:
        socket.create_connection((u.hostname, u.port or 4723), timeout=2).close()
        return True
    except OSError:
        return False


@pytest.mark.skipif(not TARGETS, reason="No mobile target enabled in config/mobile_targets.yaml")
@pytest.mark.skipif(not _appium_up(), reason=f"Appium server not reachable at {APPIUM_URL}")
@pytest.mark.parametrize("target", TARGETS, ids=[t["name"] for t in TARGETS])
def test_mobile_flow_reaches_second_factor(target):
    driver = create_driver(target, os.getenv("ANDROID_UDID") or None)
    out = REPORTS / "videos"
    out.mkdir(parents=True, exist_ok=True)
    driver.start_recording_screen()
    try:
        run_steps(driver, target["steps"])
        _wait(driver, target["otp_locator"])
        driver.save_screenshot(str(REPORTS / f"{target['name']}-second-factor.png"))
    finally:
        video = driver.stop_recording_screen()
        (out / f"{target['name']}.mp4").write_bytes(base64.b64decode(video))
        driver.quit()
