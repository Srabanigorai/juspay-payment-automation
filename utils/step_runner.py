"""Executes declarative web steps from config/targets.yaml with Playwright.

Keeps site-specific selectors out of test code: adapting to a new site means
editing YAML, not Python.
"""
from playwright.sync_api import Page, expect

from config.settings import DEFAULT_TIMEOUT_MS


def _scope(page: Page, step: dict):
    frame = step.get("frame")
    return page.frame_locator(frame) if frame else page


def run_steps(page: Page, steps: list[dict]) -> None:
    for i, step in enumerate(steps, 1):
        action = step["action"]
        label = step.get("note", f"{action} {step.get('selector', step.get('value', ''))}")
        print(f"  step {i}: {label}")
        if action == "goto":
            page.goto(step["value"], wait_until="domcontentloaded")
        elif action == "click":
            _scope(page, step).locator(step["selector"]).first.click()
        elif action == "fill":
            _scope(page, step).locator(step["selector"]).first.fill(step["value"])
        elif action == "type":  # key-by-key, for masked/auto-formatting fields
            _scope(page, step).locator(step["selector"]).first.press_sequentially(step["value"], delay=60)
        elif action == "select":
            _scope(page, step).locator(step["selector"]).first.select_option(step["value"])
        elif action == "press":
            _scope(page, step).locator(step["selector"]).first.press(step["value"])
        elif action == "wait_for":
            expect(_scope(page, step).locator(step["selector"]).first).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
        elif action == "pause":
            page.wait_for_timeout(int(step["value"]))
        else:
            raise ValueError(f"Unknown action: {action}")
