"""Capture genuine Flask interface evidence using an installed Chromium."""

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--chromium", help="Optional path to an installed Chromium executable")
parser.add_argument("--live", action="store_true", help="Require a successful Watson result")
args = parser.parse_args()
output = Path(__file__).resolve().parent / "evidence"
output.mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path=args.chromium)
    page = browser.new_page(viewport={"width": 1280, "height": 1000}, device_scale_factor=1)
    page.goto("http://127.0.0.1:5000", wait_until="networkidle")
    if args.live:
        page.locator("#textToAnalyze").fill("I love this new technology.")
        page.get_by_role("button", name="Analyze emotion").click()
        page.wait_for_function(
            "document.querySelector('#system_response').textContent.includes('dominant emotion')",
            timeout=90000,
        )
    page.screenshot(path=str(output / "6b_deployment_test.png"), full_page=True)
    page.locator("#textToAnalyze").fill("")
    page.get_by_role("button", name="Analyze emotion").click()
    page.get_by_text("Invalid text! Please try again!", exact=True).wait_for()
    page.screenshot(path=str(output / "7c_error_handling_interface.png"), full_page=True)
    browser.close()
print("Saved deployment and blank-input screenshots to", output)
