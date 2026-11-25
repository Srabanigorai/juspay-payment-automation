"""Central place for paths and environment-driven settings."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
VIDEOS = ROOT / "videos"

try:  # optional: load .env if python-dotenv is installed
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:  # fall back to a tiny parser so no extra dependency is needed
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

APPIUM_URL = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
DEFAULT_TIMEOUT_MS = int(os.getenv("DEFAULT_TIMEOUT_MS", "15000"))
# Browser automation settings
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

SLOW_MO_MS = int(os.getenv("SLOW_MO_MS", "0"))

VIDEO_DIR = VIDEOS

# Android configuration
ANDROID_DEVICE_NAME = os.getenv(
    "ANDROID_DEVICE_NAME",
    "Android Emulator"
)