"""
conftest.py
===========
Single source of truth for:
  - All pytest fixtures
  - JSON result saving  (was split across two files before — caused the bug)
  - AI Coach auto-run after session
  - Dashboard JSON sync

FIX: Previously json_reporter.py had its OWN pytest_sessionfinish hook AND
conftest.py had another one. pytest only reliably calls ONE of them.
Solution: everything lives here in one place. json_reporter.py now only
defines the collection class, NOT the hook.
"""

import os
import json
import time
import subprocess
from datetime import datetime

import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

# ── In-memory result collector ────────────────────────────────────────────────
# Simple list that every test appends to. No plugin conflict possible.
_RESULTS   = []
_START     = time.time()
_STARTED   = datetime.now().isoformat()


# ── pytest hook: collect each test result ─────────────────────────────────────
def pytest_runtest_logreport(report):
    """Called by pytest after every test phase. We only care about 'call' = actual test."""
    if report.when != "call":
        return

    error_msg = None
    if report.failed and report.longrepr:
        lines = str(report.longrepr).strip().split("\n")
        error_msg = lines[-1][:200]   # last line of traceback, max 200 chars

    _RESULTS.append({
        "name":     report.nodeid.split("::")[-1],
        "nodeid":   report.nodeid,
        "file":     report.nodeid.split("::")[0].replace("\\", "/").split("/")[-1],
        "status":   "pass" if report.passed else ("fail" if report.failed else "skip"),
        "duration": round(report.duration, 2),
        "error":    error_msg,
    })


# ── pytest hook: after ALL tests finish ───────────────────────────────────────
def pytest_sessionfinish(session, exitstatus):
    """
    Runs once at the very end.
    1. Saves reports/results.json
    2. Copies it to dashboard/results.json  (so dashboard loads it)
    3. Runs AI Coach in terminal
    """
    if not _RESULTS:
        return

    total   = len(_RESULTS)
    passed  = sum(1 for r in _RESULTS if r["status"] == "pass")
    failed  = sum(1 for r in _RESULTS if r["status"] == "fail")
    skipped = total - passed - failed
    dur     = round(time.time() - _START, 1)

    report = {
        "session": {
            "started_at":  _STARTED,
            "finished_at": datetime.now().isoformat(),
            "duration_s":  dur,
        },
        "summary": {
            "total":     total,
            "passed":    passed,
            "failed":    failed,
            "skipped":   skipped,
            "pass_rate": round(passed / total * 100, 1) if total else 0,
        },
        "tests":    _RESULTS,
        "failures": [r for r in _RESULTS if r["status"] == "fail"],
    }

    # Save to reports/
    os.makedirs("reports", exist_ok=True)
    results_path = os.path.join("reports", "results.json")
    with open(results_path, "w") as f:
        json.dump(report, f, indent=2)

    # Sync copy to dashboard/ so dashboard/index.html can fetch it
    os.makedirs("dashboard", exist_ok=True)
    dash_path = os.path.join("dashboard", "results.json")
    with open(dash_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n  Results saved → reports/results.json + dashboard/results.json")

    # Run AI Coach
    print("\n" + "=" * 55)
    print("  SHOPTEST PRO — AI COACH")
    print("=" * 55)
    _run_coach(report)


def _run_coach(report):
    """Print AI Coach guidance inline (no subprocess needed — avoids timing issues)."""
    s  = report["summary"]
    fails = report["failures"]

    print(f"\n  {s['passed']}/{s['total']} passed  |  "
          f"{s['failed']} failed  |  {s['pass_rate']}% pass rate  |  "
          f"{report['session']['duration_s']}s\n")

    if s["failed"] == 0:
        print("  All tests passing! Great work.\n")
        _slow_tests(report["tests"])
        print("  Tip: Run  start dashboard\\index.html  to open the dashboard.")
        return

    ERROR_PATTERNS = [
        ("TimeoutError",
         "Element not found (TimeoutError)",
         "Locator is wrong or element never appeared on page.",
         ["Run: playwright codegen <url>  to find the correct locator",
          "Check if the element is inside an <iframe>",
          "Increase timeout: page.set_default_timeout(60000)"]),

        ("to_have_url",
         "Page URL did not match expected",
         "The page navigated to a different URL than expected. "
         "Most likely your .env BASE_URL is wrong.",
         ["Open your .env file and check BASE_URL",
          "Make sure BASE_URL=https://www.saucedemo.com  (not demoqa or anything else)",
          "Delete .pytest_cache folder and run pytest again"]),

        ("AssertionError",
         "Assertion failed — value mismatch",
         "Element was found but its text/state differed from expected.",
         ["Print actual value: print(page.locator('.element').inner_text())",
          "Update the expected value in your assert to match reality",
          "Check if website text changed (e.g. 'Sign In' instead of 'Login')"]),

        ("net::ERR",
         "Network error — URL unreachable",
         "Browser could not connect. URL is wrong or server is down.",
         ["Check BASE_URL in .env file",
          "Open the URL manually in Chrome to verify it works",
          "If localhost: make sure your dev server is running"]),

        ("404",
         "API 404 — endpoint not found",
         "API test hitting an endpoint that does not exist.",
         ["Verify endpoint path in the test file",
          "Check API_BASE_URL in .env"]),
    ]

    print(f"  FAILURES — what went wrong and how to fix:\n")
    for i, fail in enumerate(fails, 1):
        error = fail.get("error") or ""
        matched = next((p for p in ERROR_PATTERNS if p[0].lower() in error.lower()), None)

        print(f"  [{i}] {fail['name']}  ({fail['file']})  — {fail['duration']}s")
        if matched:
            _, title, cause, steps = matched
            print(f"       Problem : {title}")
            print(f"       Cause   : {cause}")
            print(f"       Fix:")
            for step in steps:
                print(f"         • {step}")
        else:
            print(f"       Error   : {error or 'see reports/report.html'}")
            print(f"       Fix     : Open reports/report.html for full traceback")
        print()

    _slow_tests(report["tests"])

    print("  QUICK COMMANDS:")
    print("    pytest --last-failed -v          ← run only failed tests")
    print("    start reports\\report.html        ← open HTML report")
    print("    start dashboard\\index.html       ← open analytics dashboard")
    print()


def _slow_tests(tests):
    slow = [t for t in tests if t["duration"] > 15]
    if not slow:
        return
    print("  SLOW TESTS (>15s — consider optimising):")
    for t in sorted(slow, key=lambda x: x["duration"], reverse=True):
        print(f"    • {t['name']}  ({t['duration']}s)")
        print(f"      Tip: Use auth_state fixture to skip re-login per test")
    print()


# ── Shared fixtures ───────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://www.saucedemo.com")


@pytest.fixture(scope="session")
def credentials():
    return {
        "username":    os.getenv("STANDARD_USER", "standard_user"),
        "password":    os.getenv("PASSWORD",       "secret_sauce"),
        "locked_user": os.getenv("LOCKED_USER",    "locked_out_user"),
    }


@pytest.fixture(scope="session")
def api_base_url():
    return os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def auth_state(tmp_path_factory, base_url, credentials):
    """Log in once, save browser storage state — reused by all tests that need auth."""
    state_file = tmp_path_factory.mktemp("auth") / "state.json"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page    = context.new_page()
        page.goto(base_url)
        page.get_by_placeholder("Username").fill(credentials["username"])
        page.get_by_placeholder("Password").fill(credentials["password"])
        page.get_by_role("button", name="Login").click()
        page.wait_for_url("**/inventory.html")
        context.storage_state(path=str(state_file))
        browser.close()
    return str(state_file)
