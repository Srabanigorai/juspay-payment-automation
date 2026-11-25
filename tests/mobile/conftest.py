import base64
import time

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.settings import ANDROID_DEVICE_NAME, APPIUM_URL, VIDEO_DIR


@pytest.fixture
def driver(request):
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.device_name = ANDROID_DEVICE_NAME
    opts.browser_name = "Chrome"  # mobile web; for a native app set opts.app / app_package instead
    opts.new_command_timeout = 300
    drv = webdriver.Remote(APPIUM_URL, options=opts)
    drv.start_recording_screen()
    yield drv
    video = drv.stop_recording_screen()
    out = VIDEO_DIR / "mobile"
    out.mkdir(exist_ok=True)
    (out / f"{request.node.name}_{int(time.time())}.mp4").write_bytes(base64.b64decode(video))
    drv.quit()
