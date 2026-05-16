# ShopTest Pro v3 — Complete & Fixed

All v1 tests + v2 analytics + all bugs fixed.


Complete E2E test automation framework: **all v1 tests + v2 analytics + AI coach + URL analyser**. Nothing removed, everything combined.

---

## What's included

### From v1 (original — all present)
- `pages/` — 4 Page Object Models (Login, Inventory, Cart, Checkout)
- `tests/ui/` — 20 UI tests (login, inventory, checkout)
- `tests/api/` — 12 API tests (GET, POST, PUT, DELETE, parametrized)
- `conftest.py` — shared fixtures, auth state reuse
- `pytest.ini` — markers, HTML report config
- `.github/workflows/` — CI/CD on Chromium + Firefox

### From v2 (new — all present)
- `utils/json_reporter.py` — captures results to reports/results.json after every run
- `utils/ai_coach.py` — reads failures, explains what went wrong, gives fix steps
- `utils/url_analyser.py` — scans any URL, detects forms/cart/login, recommends tests
- `dashboard/index.html` — visual charts (pass rate, slowest tests, AI coach, URL analyser)

---



## All commands

```bash
# Run all 32 tests
pytest -v

# Run only smoke tests (fast, ~2 min)
pytest -m smoke -v

# Run only API tests
pytest -m api -v

# Run on Firefox
pytest --browser firefox -v

# Run headless (no browser window)
pytest --headed=false -v

# Analyse any website before writing tests
python utils/url_analyser.py https://yourwebsite.com

# Run AI Coach manually
python utils/ai_coach.py

# Open dashboard (after running tests)
open dashboard/index.html
```


---

## Test coverage (32 tests)

| File | Tests | Type |
|------|-------|------|
| test_login.py | 7 | smoke + negative + parametrized |
| test_inventory.py | 9 | smoke + regression |
| test_checkout.py | 9 | smoke + negative + parametrized |
| test_api.py | 12 | smoke + CRUD + parametrized |
| **Total** | **32** | |

## Bugs fixed in this version
1. **AI Coach not showing** — JSON reporter and conftest.py had conflicting `pytest_sessionfinish` hooks. Fixed by putting everything in one place inside conftest.py.
2. **BASE_URL pointing to demoqa** — .env now correctly set to saucedemo.com.
3. **Dashboard not loading** — results.json now auto-copied to dashboard/ folder after every run, and dashboard auto-refreshes every 30s.
4. **`assert_logged_in` URL pattern** — changed from wildcard to exact URL to avoid false failures.

## Quick start
```bash
pip install -r requirements.txt
playwright install
pytest -v
```
After tests finish:
- AI Coach prints automatically in the terminal
- Open `dashboard/index.html` in your browser — it loads results automatically

## All commands
```bash
pytest -v                                              # run everything
pytest -m smoke -v                                     # smoke only (fast)
pytest -m api -v                                       # API only (no browser)
pytest --browser firefox -v                            # run on Firefox
pytest --headed=false -v                               # headless mode
pytest --last-failed -v                                # only failed tests
pytest tests/ui/test_login.py -v                       # one file
pytest tests/ui/test_login.py::test_valid_login -v    # one test
python utils/ai_coach.py                               # manual coach run
python utils/url_analyser.py https://yoursite.com      # analyse new website
start dashboard\index.html                             # open dashboard (Windows)
```

## NEW Project structure
```
shoptest_v3/
├── pages/                    ← Page Object Models
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── ui/
│   │   ├── test_login.py       (7 tests)
│   │   ├── test_inventory.py   (9 tests)
│   │   └── test_checkout.py    (9 tests)
│   └── api/
│       └── test_api.py         (13 tests)
├── utils/
│   ├── ai_coach.py             ← manual coach runner
│   └── url_analyser.py         ← scan any website
├── dashboard/
│   └── index.html              ← analytics dashboard
├── conftest.py                 ← fixtures + auto AI Coach + JSON save
├── pytest.ini
├── requirements.txt
└── .env
```
