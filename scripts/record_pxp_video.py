
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

BASE_DIR = Path(__file__).resolve().parents[1]
VIDEO_DIR = BASE_DIR / "videos" / "automated"
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

PXP_URL = "https://demo.pxp.io/dropin"


def run():
    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=700
        )

        context = browser.new_context(
            ignore_https_errors=True,
            record_video_dir=str(VIDEO_DIR),
            record_video_size={
                "width": 1280,
                "height": 720
            }
        )

        page = context.new_page()

        try:
            print("Opening PXP demo...")
            page.goto(PXP_URL, wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")

            print("Selecting product...")
            page.get_by_role(
                "button", name="plus Cart"
            ).nth(2).click()

            print("Opening cart...")
            page.get_by_role(
                "link", name="shopping-cart"
            ).click()

            print("Proceeding to checkout...")
            page.get_by_role(
                "button", name="arrow-right Proceed to"
            ).click()

            print("Selecting Card payment...")
            page.get_by_label(
                "Payment method Card"
            ).click()

            print("Waiting for card form...")
            page.wait_for_timeout(3000)

            
            card_frames = [
                frame for frame in page.frames
                if frame != page.main_frame
            ]

            print(
                "Detected iframe count:",
                len(card_frames)
            )

            print(
                "Please inspect the card fields "
                "before proceeding with payment."
            )

            page.pause()

        

        except Exception as error:
            print("Automation failed:", error)
            raise

        finally:
            print("Closing browser and saving video...")
            context.close()
            browser.close()

            print("Video folder:", VIDEO_DIR)


if __name__ == "__main__":
    run()
