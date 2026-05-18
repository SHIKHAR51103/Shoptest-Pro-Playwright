# 🎭 ShopTest Pro

> A complete, production-grade **Test Automation Framework** built with **Playwright + Python**.
> Covers UI automation, API testing, Page Object Model, data-driven testing, CI/CD pipeline, analytics dashboard, and an AI Coach that tells you exactly what went wrong and how to fix it.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.44-green?logo=playwright)
![pytest](https://img.shields.io/badge/pytest-8.2-orange)
![Tests](https://img.shields.io/badge/Tests-38%20passing-brightgreen)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black?logo=github)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Table of Contents

- [What is this project?](#-what-is-this-project)
- [What does it test?](#-what-does-it-test)
- [Tech stack](#-tech-stack)
- [Project structure explained](#-project-structure-explained)
- [How to set up locally](#-how-to-set-up-locally)
- [How to run tests](#-how-to-run-tests)
- [Understanding test results](#-understanding-test-results)
- [AI Coach](#-ai-coach)
- [Analytics Dashboard](#-analytics-dashboard)
- [URL Analyser](#-url-analyser)
- [Page Object Model explained](#-page-object-model-explained)
- [How CI/CD works](#-how-cicd-works)
- [How to test a different website](#-how-to-test-a-different-website)
- [Common errors and fixes](#-common-errors-and-fixes)
- [Test coverage](#-test-coverage)

---

## 🤔 What is this project?

This is a **test automation framework** — a system that automatically checks whether a website is working correctly, without a human having to click through it manually every time.

Think of it this way: every time a developer changes the code of a website, something might break. Instead of a human manually checking every button, form, and page, this framework does it automatically in minutes — and tells you exactly what broke and why.

**This project tests two things:**

1. **UI (User Interface)** — Opens a real browser, clicks buttons, fills forms, and checks what happens on screen. Just like a real user would.
2. **API (Application Programming Interface)** — Sends requests directly to the server (like Postman does) and checks the responses, without opening a browser.

**The website being tested:** [SauceDemo](https://www.saucedemo.com) — a free, public demo e-commerce website made specifically for practising test automation.

**The API being tested:** [JSONPlaceholder](https://jsonplaceholder.typicode.com) — a free, public fake REST API used for practice.

---

## 🛒 What does it test?

### UI Tests (Browser-based)

| Flow | What is tested |
|------|----------------|
| **Login** | Valid login, locked-out user, empty fields, wrong password |
| **Products page** | Page loads with 6 products, sorting by name A→Z / Z→A, sorting by price low→high / high→low |
| **Cart** | Adding items, removing items, cart badge count updates correctly |
| **Checkout** | Complete purchase flow, missing first name / last name / zip code validation |

### API Tests (No browser)

| Endpoint | What is tested |
|----------|----------------|
| `GET /posts` | Returns 100 posts with status 200 |
| `GET /posts/1` | Returns correct post with all required fields |
| `GET /posts/9999` | Returns 404 for non-existent resource |
| `POST /posts` | Creates a new post, returns 201 |
| `PUT /posts/1` | Updates an existing post |
| `DELETE /posts/1` | Deletes a post |
| `GET /users` | Returns 10 users, all with valid email addresses |

---

## 🛠 Tech stack

| Tool | Version | What it does |
|------|---------|--------------|
| **Python** | 3.9+ | Programming language used to write all tests |
| **Playwright** | 1.44 | Opens browsers and automates clicks, typing, and navigation |
| **pytest** | 8.2 | Test runner — discovers, runs, and reports all test results |
| **pytest-playwright** | 0.5 | Connects pytest and Playwright — gives ready-made fixtures like `page` |
| **pytest-html** | 4.1 | Generates a beautiful HTML report after every test run |
| **Faker** | 25.2 | Generates realistic random test data (names, addresses, zip codes) |
| **python-dotenv** | 1.0 | Loads credentials from `.env` file — keeps passwords out of code |
| **GitHub Actions** | — | Runs tests automatically on every code push (CI/CD) |

---

## 📁 Project structure explained

```
shoptest_v3/
│
├── 📂 pages/                        ← Page Object Models
│   ├── login_page.py                   Handles login form interactions
│   ├── inventory_page.py               Handles products page interactions
│   ├── cart_page.py                    Handles shopping cart interactions
│   └── checkout_page.py                Handles checkout flow interactions
│
├── 📂 tests/
│   ├── 📂 ui/                       ← Browser tests (open a real browser)
│   │   ├── test_login.py               7 login tests
│   │   ├── test_inventory.py           9 product/cart tests
│   │   └── test_checkout.py            9 E2E checkout tests
│   └── 📂 api/                      ← API tests (no browser needed)
│       └── test_api.py                 13 REST API tests
│
├── 📂 utils/
│   ├── ai_coach.py                  ← Reads failures, explains what to fix
│   └── url_analyser.py              ← Scans any URL, recommends tests
│
├── 📂 dashboard/
│   ├── index.html                   ← Visual analytics dashboard
│   └── results.json                 ← Auto-generated after every test run
│
├── 📂 reports/
│   ├── report.html                  ← HTML test report (auto-generated)
│   └── results.json                 ← Raw test data for the dashboard
│
├── conftest.py                      ← Shared setup: fixtures + result saving + AI Coach
├── pytest.ini                       ← pytest settings and marker definitions
├── requirements.txt                 ← All Python packages to install
├── .env                             ← Credentials (never upload to GitHub)
├── .gitignore                       ← Files Git should ignore
└── .github/
    └── workflows/
        └── playwright_tests.yml     ← GitHub Actions CI/CD pipeline
```

### What does each folder actually do?

**`pages/`** — This is the heart of the framework. Each file represents one page of the website. Instead of writing locators (how to find a button) inside every test, we write them once here. If the website changes, you fix it in one file only.

**`tests/`** — These files contain the actual test cases. They use the Page Objects from `pages/` — tests describe *what* to test, not *how* to find elements.

**`utils/`** — Helper tools. The AI Coach reads your test results and explains failures. The URL Analyser scans any website and tells you what tests to write.

**`dashboard/`** — A visual HTML page showing charts, pass rates, and failure analysis. Open in any browser after running tests.

**`conftest.py`** — The most important configuration file. It runs before any test, sets up shared data (like credentials), and after all tests finish, it saves results and runs the AI Coach automatically.

---

## ⚙ How to set up locally

### Prerequisites

- Python 3.9 or higher installed → [Download Python](https://python.org)
- Git installed → [Download Git](https://git-scm.com)
- PyCharm or any code editor

### Step 1 — Clone the repository

```bash
git clone https://github.com/SHIKHAR51103/Shoptest-Pro-Playwright.git
cd Shoptest-Pro-Playwright
```

### Step 2 — Create a virtual environment

A virtual environment keeps this project's packages separate from other Python projects.

```bash
# Create venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal line.

### Step 3 — Install all dependencies

```bash
pip install -r requirements.txt
```

This installs pytest, Playwright, Faker, and all other required packages from the list in `requirements.txt`.

### Step 4 — Install browsers

Playwright needs to download the actual browser files (Chromium, Firefox, WebKit).

```bash
playwright install
```

This takes 2–3 minutes. You will see download progress. This only needs to be done once.

### Step 5 — Set up credentials

The `.env` file contains login credentials. It is already configured for the default test site:

```
BASE_URL=https://www.saucedemo.com
STANDARD_USER=standard_user
LOCKED_USER=locked_out_user
PASSWORD=secret_sauce
API_BASE_URL=https://jsonplaceholder.typicode.com
```

> ⚠️ Never change this file to contain real passwords. Never commit `.env` to GitHub — it is already in `.gitignore`.

---

## ▶ How to run tests

### Run everything

```bash
pytest -v
```

A Chrome browser window will open. You will see it clicking, typing, and navigating by itself. Each test name appears in the terminal with `PASSED` or `FAILED`. After all tests finish, the AI Coach runs automatically.

### Run specific test types

```bash
# Only smoke tests — fastest, ~2 minutes, covers critical paths
pytest -m smoke -v

# Only API tests — no browser opens, very fast
pytest -m api -v

# Only UI tests — browser opens
pytest -m ui -v

# Only one specific file
pytest tests/ui/test_login.py -v

# Only one specific test
pytest tests/ui/test_login.py::test_valid_login -v

# Only tests that failed last time
pytest --last-failed -v
```

### Change the browser

```bash
# Run on Firefox
pytest --browser firefox -v

# Run on WebKit (Safari engine)
pytest --browser webkit -v

# Run without browser window opening (faster)
pytest --headed=false -v
```

### Open reports after running

```bash
# Windows — open HTML report
start reports\report.html

# Windows — open dashboard
start dashboard\index.html

# Mac
open reports/report.html
open dashboard/index.html
```

---

## 📊 Understanding test results

After `pytest -v` runs, you will see output like this in the terminal:

```
tests/api/test_api.py::test_get_all_posts PASSED        [  2%]
tests/api/test_api.py::test_get_single_post PASSED      [  5%]
tests/ui/test_login.py::test_valid_login[chromium] PASSED  [ 81%]
tests/ui/test_login.py::test_logout[chromium] PASSED    [100%]

========= 38 passed in 433s =========
```

**What the markers mean:**

| Marker | Meaning |
|--------|---------|
| `PASSED` | Test ran and everything was as expected ✅ |
| `FAILED` | Test ran but something was wrong ❌ |
| `ERROR` | Test could not even start (setup problem) 🔴 |
| `SKIPPED` | Test was intentionally skipped ⏭ |
| `[chromium]` | This UI test ran on the Chromium browser |

**The percentage** `[  2%]` shows how far through the total test suite you are.

---

## 🤖 AI Coach

The AI Coach is the most unique feature of this framework. It runs **automatically** after every `pytest` run — you do not need to do anything.

### What it does

After all tests finish, it reads the results and prints a report like this in your terminal:

```
=======================================================
  SHOPTEST PRO — AI COACH
=======================================================

  36/38 passed  |  2 failed  |  94.7% pass rate  |  433s

  FAILURES — what went wrong and how to fix:

  [1] test_valid_login  (test_login.py)  — 5.2s
       Problem : URL mismatch
       Cause   : BASE_URL in .env is pointing to the wrong site
       Fix:
         • Open .env and set BASE_URL=https://www.saucedemo.com
         • Delete .pytest_cache and run pytest again

  QUICK COMMANDS:
    pytest --last-failed -v          ← run only failed tests
    start reports\report.html        ← open HTML report
    start dashboard\index.html       ← open analytics dashboard
```

### Run it manually any time

```bash
python utils/ai_coach.py
```

### Error patterns it recognises

| Error | What it tells you |
|-------|------------------|
| `TimeoutError` | Locator is wrong, gives steps to find correct one |
| `to_have_url` mismatch | Wrong BASE_URL in `.env` |
| `AssertionError` | Value mismatch, tells you how to print actual value |
| `net::ERR` | Network unreachable, tells you to check URL |
| `404` | API endpoint wrong, tells you to verify path |

---

## 📈 Analytics Dashboard

After running `pytest -v`, open the dashboard in your browser:

```bash
start dashboard\index.html    # Windows
open dashboard/index.html     # Mac
```

### What the dashboard shows

**4 metric cards at the top:**
- Total tests run
- How many passed (with percentage)
- How many failed
- Total duration

**Pass rate ring chart** — Visual circle showing overall pass percentage. Green = 90%+, Yellow = 70–90%, Red = below 70%.

**Category bars** — Pass rate broken down by Login / Inventory / Checkout / API sections.

**Slowest tests bar chart** — Horizontal bar chart showing the 8 slowest tests. Red bars = failed, Green bars = passed. Useful for spotting performance issues.

**AI Coach panel** — Same failure analysis as the terminal, but in a visual card format with colour coding.

**Test results table** — Every single test with pass/fail dot, file name, and duration. Filter by All / Passed / Failed / UI / API.

**URL Analyser** — Paste any website URL and get instant recommendations on what to test.

> 💡 The dashboard **auto-refreshes every 30 seconds** — so if you keep it open while running tests, results appear automatically.

---

## 🔍 URL Analyser

Whenever you need to test a **new website**, run this tool first:

```bash
python utils/url_analyser.py https://the-new-website.com
```

### What it does

It opens the website in a headless browser, scans the page, and prints:

```
=======================================================
  ShopTest Pro — URL Analyser
  Scanning: https://example.com
=======================================================

  HTTP Status : 200
  Page Title  : Example Shop

  FEATURES DETECTED
  ─────────────────────────────────────────
  + Login Form
  + Search Box
  + Cart
  + Dropdown

  TEST RECOMMENDATIONS
  ─────────────────────────────────────────

  [Login form detected]
  Tests to write:
    - test_valid_login — correct credentials should reach dashboard
    - test_invalid_login — wrong password should show error message
    - test_empty_fields — blank form should show validation error
  POM advice : Create pages/login_page.py with username, password, submit, error locators
  Watch out  : Use get_by_placeholder() not CSS ids — more stable

  NEXT STEPS
  ─────────────────────────────────────────
  1. Update .env:  BASE_URL=https://example.com
  2. Run: playwright codegen https://example.com
  3. Update locators in pages/ folder
  4. Run: pytest -v
```

---

## 🏗 Page Object Model explained

The Page Object Model (POM) is a design pattern that makes test code clean, readable, and maintainable.

### The problem without POM

Imagine the login button's HTML id changes from `#login-button` to `#btn-login`. Without POM, you would need to find and fix this in every single test file.

```python
# BAD — locator written directly inside test
def test_login(page):
    page.locator("#user-name").fill("standard_user")    # ← hardcoded
    page.locator("#password").fill("secret_sauce")       # ← hardcoded
    page.locator("#login-button").click()                # ← hardcoded
```

### The solution with POM

```python
# pages/login_page.py — locators written ONCE here
class LoginPage:
    def __init__(self, page):
        self.username_input = page.get_by_placeholder("Username")  # defined once
        self.password_input = page.get_by_placeholder("Password")  # defined once
        self.login_button   = page.get_by_role("button", name="Login")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

# tests/ui/test_login.py — test is clean, no locators here
def test_valid_login(page, credentials):
    LoginPage(page).navigate().login(credentials["username"], credentials["password"])
```

If the button changes, you fix it in `login_page.py` only. All tests automatically work again.

### The 4 Page Objects in this project

| File | Page it represents | Key locators |
|------|--------------------|--------------|
| `login_page.py` | `saucedemo.com/` | username input, password input, login button, error message |
| `inventory_page.py` | `saucedemo.com/inventory.html` | sort dropdown, product names, prices, cart badge, cart icon |
| `cart_page.py` | `saucedemo.com/cart.html` | cart items, item names, checkout button |
| `checkout_page.py` | Checkout steps 1, 2, and complete | first name, last name, zip, continue, finish, order confirmation |

---

## ⚡ How CI/CD works

CI/CD stands for **Continuous Integration / Continuous Deployment**. It means tests run automatically every time you push code to GitHub — without you doing anything.

### The workflow file

`.github/workflows/playwright_tests.yml` tells GitHub what to do.

### What happens step by step when you run `git push`

```
You push code to GitHub
        ↓
GitHub reads playwright_tests.yml
        ↓
GitHub creates a fresh Ubuntu machine in the cloud (free)
        ↓
Installs Python 3.11 + all packages from requirements.txt
        ↓
Downloads Chromium and Firefox browsers
        ↓
Runs smoke tests first (fast gate — if these fail, stops here)
        ↓
If smoke passes → runs all 38 tests on Chromium
At the same time → runs all 38 tests on Firefox (parallel)
        ↓
Saves HTML reports as downloadable artifacts
If any test failed → saves Playwright traces for debugging
        ↓
Shows green ✓ or red ✗ on your GitHub repository page
```

### How to see CI results on GitHub

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You see every run with pass/fail status
4. Click any run → click any job → see the full test output
5. Scroll to **Artifacts** → download the HTML report

> 💡 A green checkmark on your GitHub repo means all tests are passing — this is what companies look for.

---

## 🌐 How to test a different website

Follow these 6 steps every time you get a new website to test.

### Step 1 — Analyse the website

```bash
python utils/url_analyser.py https://new-website.com
```

Read the output — it tells you what Page Objects to create and what tests to write.

### Step 2 — Record using Playwright codegen

```bash
playwright codegen https://new-website.com
```

A browser opens. Click around — login, add items, fill forms. Playwright writes the Python code for you in a side panel. Copy the locators from there.

### Step 3 — Update `.env`

```
BASE_URL=https://new-website.com
STANDARD_USER=your_test_username
PASSWORD=your_test_password
```

### Step 4 — Update Page Objects

Open each file in `pages/` and replace the locators with ones from codegen output. Example:

```python
# If new site uses "Email" instead of "Username":
self.username_input = page.get_by_placeholder("Email")   # changed
```

Only change locators inside `pages/` — test files stay the same.

### Step 5 — Run tests

```bash
pytest tests/ui/test_login.py -v    # start with login only
```

Fix any failures, then gradually run more test files.

### Step 6 — Follow AI Coach output

The AI Coach tells you exactly what locator is wrong and how to fix it. Follow its steps.

---

## 🐛 Common errors and fixes

### `error: src refspec main does not match any`

**Cause:** You tried to push without doing `git add` and `git commit` first.

**Fix:**
```bash
git add .
git commit -m "feat: initial commit"
git push -u origin main
```

---

### `TimeoutError: Timeout 30000ms exceeded`

**Cause:** Playwright couldn't find the element on the page. The locator is wrong.

**Fix:**
```bash
playwright codegen https://www.saucedemo.com
```
Record the correct locator and update it in the relevant `pages/` file.

---

### `AssertionError: Page URL expected to be 'https://demoqa.com/...'`

**Cause:** Your `.env` file has the wrong `BASE_URL`.

**Fix:** Open `.env` and set:
```
BASE_URL=https://www.saucedemo.com
```

---

### `No results.json found` when running AI Coach manually

**Cause:** Tests haven't been run yet, or the run was interrupted.

**Fix:**
```bash
pytest -v    # run tests first, then coach runs automatically
```

---

### `ModuleNotFoundError: No module named 'playwright'`

**Cause:** Virtual environment is not activated or packages not installed.

**Fix:**
```bash
venv\Scripts\activate         # activate venv first
pip install -r requirements.txt
```

---

### `git push` asks for password but token doesn't work

**Cause:** The Personal Access Token may have expired or been typed wrong.

**Fix:** Generate a new token on GitHub:
- GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic) → Generate new token
- Tick the `repo` checkbox → Generate → Copy immediately
- Use this as your password when Git prompts

---

## 📋 Test coverage

| File | Tests | Markers | Description |
|------|-------|---------|-------------|
| `test_login.py` | 7 | smoke, ui | Valid login, locked user, empty fields, parametrized invalid combos, logout |
| `test_inventory.py` | 9 | smoke, ui | Page load, 4 sort options, add/remove cart items |
| `test_checkout.py` | 9 | smoke, ui | Single + multiple item purchase, 3 validation tests, 3 parametrized addresses |
| `test_api.py` | 13 | smoke, api | GET, POST, PUT, DELETE, 404, comments, users, 5 parametrized post IDs |
| **Total** | **38** | | |

### Test markers

| Marker | Purpose | How to run |
|--------|---------|------------|
| `smoke` | Critical path tests — run before every deploy | `pytest -m smoke -v` |
| `ui` | All browser-based tests | `pytest -m ui -v` |
| `api` | All API tests — no browser needed | `pytest -m api -v` |
| `regression` | Full suite for thorough checking | `pytest -v` |

---

## 👨‍💻 Author

**Shikhar Agarwal**
Software Test Trainee | Playwright + Python Automation

- GitHub: [@SHIKHAR51103](https://github.com/SHIKHAR51103)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

*Built with ❤️ to demonstrate SDET-level automation skills: Page Object Model, data-driven testing, API testing, CI/CD integration, and intelligent failure analysis.*
