"""
utils/ai_coach.py
=================
Reads reports/results.json and prints guidance.

The AI Coach now runs AUTOMATICALLY after every pytest session via conftest.py.
This file is for MANUAL runs only:
    python utils/ai_coach.py
"""

import json
import os
import sys

# Add project root to path so this runs from any directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


ERROR_PATTERNS = [
    ("TimeoutError",
     "Element not found (TimeoutError)",
     "Locator is wrong or element never appeared on page.",
     ["Run: playwright codegen <url>  to find the correct locator",
      "Check if element is inside an <iframe>",
      "Increase timeout: page.set_default_timeout(60000)"]),

    ("to_have_url",
     "Page URL did not match expected",
     "BASE_URL in .env is likely pointing to the wrong site.",
     ["Open .env and verify: BASE_URL=https://www.saucedemo.com",
      "Delete .pytest_cache and run pytest again"]),

    ("AssertionError",
     "Assertion failed — value mismatch",
     "Element found but its text/state was different from expected.",
     ["Print actual: print(page.locator('.element').inner_text())",
      "Update expected value in your assert statement"]),

    ("net::ERR",
     "Network error — URL unreachable",
     "Browser could not connect to the URL.",
     ["Check BASE_URL in .env",
      "Open URL manually in Chrome to verify",
      "If localhost: start your dev server first"]),
]


def coach():
    path = os.path.join("reports", "results.json")
    if not os.path.exists(path):
        # Try dashboard folder as fallback
        path = os.path.join("dashboard", "results.json")
    if not os.path.exists(path):
        print("\n  No results.json found.")
        print("  Run tests first:  pytest -v\n")
        return

    with open(path) as f:
        data = json.load(f)

    s     = data["summary"]
    fails = data["failures"]
    sess  = data["session"]

    print(f"\n{'='*55}")
    print(f"  ShopTest Pro — AI Coach (manual run)")
    print(f"  Last run: {sess['finished_at'][:19]}  |  {sess['duration_s']}s")
    print(f"{'='*55}")
    print(f"\n  {s['passed']}/{s['total']} passed  |  {s['failed']} failed  |  {s['pass_rate']}% pass rate\n")

    if not fails:
        print("  All tests passing! Nothing to fix.\n")
        _slow_tests(data["tests"])
        return

    print("  FAILURES:\n")
    for i, fail in enumerate(fails, 1):
        error = fail.get("error") or ""
        matched = next((p for p in ERROR_PATTERNS if p[0].lower() in error.lower()), None)
        print(f"  [{i}] {fail['name']}  ({fail['file']})")
        if matched:
            _, title, cause, steps = matched
            print(f"       Problem : {title}")
            print(f"       Cause   : {cause}")
            print(f"       Fix:")
            for step in steps:
                print(f"         • {step}")
        else:
            print(f"       Error   : {error or 'open reports/report.html'}")
        print()

    _slow_tests(data["tests"])
    print("  Commands:")
    print("    pytest --last-failed -v   ← run only failed tests")
    print("    start reports\\report.html ← full HTML report\n")


def _slow_tests(tests):
    slow = [t for t in tests if t["duration"] > 15]
    if not slow:
        return
    print("  SLOW TESTS (>15s):")
    for t in sorted(slow, key=lambda x: x["duration"], reverse=True):
        print(f"    • {t['name']}  ({t['duration']}s)")
    print()


if __name__ == "__main__":
    coach()
