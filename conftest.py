import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 800},
            "locale": "en-IN", "record_video_size": {"width": 1280, "height": 800}}
