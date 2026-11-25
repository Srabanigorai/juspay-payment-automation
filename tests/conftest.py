
import pytest

from config.settings import HEADLESS, SLOW_MO_MS, VIDEO_DIR


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": HEADLESS,
        "slow_mo": SLOW_MO_MS,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    video_path = VIDEO_DIR / "web"
    video_path.mkdir(parents=True, exist_ok=True)

    return {
        **browser_context_args,
        "viewport": {"width": 1366, "height": 800},
        "record_video_dir": str(video_path),
        "record_video_size": {"width": 1280, "height": 720},
    }
