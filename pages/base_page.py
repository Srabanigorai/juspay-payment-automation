from playwright.sync_api import Page

from config.settings import REPORT_DIR
from utils.logger import get_logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger(self.__class__.__name__)

    def open(self, url: str):
        self.log.info("Opening %s", url)
        self.page.goto(url, wait_until="domcontentloaded")

    def screenshot(self, name: str):
        self.page.screenshot(path=str(REPORT_DIR / f"{name}.png"), full_page=True)
