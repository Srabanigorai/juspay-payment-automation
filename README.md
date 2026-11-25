# Payment Journey Automation

Automates payment journeys on **web (Playwright + pytest)** and **Android (Appium + pytest)**
using a Page Object Model, config-driven selectors and HTML reporting.
Each flow reaches the second-factor (OTP) page; sandbox flows also **complete the transaction**.

| Layer | Tooling |
|---|---|
| Web | Playwright (Python), pytest, pytest-html |
| Mobile | Appium 2 + UiAutomator2, Appium-Python-Client |
| Pattern | Page Objects (`pages/`), declarative live steps (`config/*.yaml`), env-based test data |
| Evidence | Per-test video + trace on failure + screenshots + HTML report |

## What is automated

| Flow | Methods | Ends at |
|---|---|---|
| Mock checkout (`tests/web/test_mock_payments.py`) | Card (inside iframe), UPI, Netbanking | OTP page, then **successful transaction** with sandbox OTP `123456` |
| Negative paths | Wrong OTP then correct, 3 wrong OTPs, declined card, Luhn-invalid card | Error states |
| Live web (`tests/web/test_live_checkout.py`) | Card, UPI (any site in `config/targets.yaml`) | Second-factor page |
| Live Android (`tests/mobile/test_mobile_payment.py`) | Card (any app in `config/mobile_targets.yaml`) | Second-factor screen |

The mock checkout (`mock_app/`) is served locally by the test run, so the framework can be
verified on any machine without internet or accounts.
## Automation Demo Video

The recorded Playwright automation execution is available at:

`videos/automated/PXP_Playwright_Automation_Demo.webm`

The video demonstrates automated product selection, cart navigation, checkout and payment form navigation.

## Prerequisites
- Python 3.10+
- For mobile only: Node.js 18+, JDK 17, Android SDK + an emulator or USB device, Appium 2

## Setup (any new machine)
```bash
git clone <your-repo-url> payment-automation && cd payment-automation
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env               # Windows: copy .env.example .env  (then fill in values)
```

## Run

**1. Mock checkout, headless:**
```bash
pytest -m mock
```
**2. Mock checkout, visible and slowed down (use this for the demo recording):**
```bash
./scripts/run_web_mock.sh          # Windows: scripts\run_web_mock.bat
```
**3. Live web target:** edit `config/targets.yaml` (find selectors with `playwright codegen <url>`),
set `enabled: true`, put your values in `.env`, then:
```bash
pytest -m live --headed --slowmo 500
```
**4. Live Android app:**
```bash
npm i -g appium && appium driver install uiautomator2
appium                                   # terminal 1: leave running
adb devices                              # confirm the emulator/device shows up
# edit config/mobile_targets.yaml (locators via Appium Inspector), set enabled: true
pytest -m mobile                         # terminal 2
```
Run everything: `pytest`. Tests with no enabled target or no Appium server are skipped, not failed.

## Outputs
- `reports/report.html`: self-contained results report
- `reports/artifacts/<test>/video.webm`: video of every web test (traces for failures)
- `reports/videos/*.mp4`: Android screen recordings
- `reports/*-second-factor.png`: screenshot at the second-factor page

Open a trace with `playwright show-trace reports/artifacts/<test>/trace.zip`.

## Project layout
```
config/      settings, targets.yaml (web), mobile_targets.yaml (Android)
pages/       CheckoutPage, OtpPage (page objects)
utils/       data loader, YAML step runners (web + mobile)
tests/       web/ and mobile/ suites
mock_app/    local sandbox checkout (card iframe, UPI, netbanking, OTP)
test_data/   test cards and OTPs (sandbox values only)
scripts/     demo-run helpers
```

## Design notes
- **Waits:** only auto-waiting Playwright locators and explicit expected conditions. No fixed sleeps in flows.
- **Iframes:** card fields are reached with `frame_locator`, as on real PSP checkouts.
- **Secrets:** nothing sensitive is committed; `.env` is git-ignored and YAML uses `${VAR}`.
- **Extensibility:** a new site means a new YAML block, not new code. A new method means a page-object method plus a test.

## Known limitations
- Live production sites may use bot detection or CAPTCHAs; the framework does not bypass them. Run headed and use your own test accounts/cards.
- Real bank OTPs cannot be automated; live flows stop at the OTP page. OTP completion is demonstrated on the sandbox checkout.
- Live selectors change over time and may need refreshing in the YAML.



