# ShopTest Pro v3 — Complete & Fixed

All v1 tests + v2 analytics + all bugs fixed.

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

## Project structure
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
