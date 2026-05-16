"""
utils/url_analyser.py
=====================
Scans any website and recommends what tests to write.
Run: python utils/url_analyser.py https://yourwebsite.com
"""

import sys
import json
import os
from playwright.sync_api import sync_playwright


ADVICE = {
    "login_form": {
        "title": "Login form detected",
        "tests": [
            "test_valid_login — correct credentials should reach dashboard",
            "test_invalid_login — wrong password should show error message",
            "test_empty_fields — blank form should show validation error",
        ],
        "pom":  "Create pages/login_page.py with username, password, submit, error locators",
        "warn": "Use get_by_placeholder() or get_by_label() — more stable than CSS ids",
    },
    "search_box": {
        "title": "Search box detected",
        "tests": [
            "test_search_valid_keyword — results should appear",
            "test_search_no_results — 'no results' message should show",
            "test_search_empty — blank search behaviour",
        ],
        "pom":  "Add search_input and search_results locators to your listing page POM",
        "warn": "Search results load dynamically — use expect(locator).to_be_visible() not sleep()",
    },
    "cart": {
        "title": "Shopping cart detected",
        "tests": [
            "test_add_to_cart — cart badge should increment",
            "test_remove_from_cart — badge should decrement",
            "test_cart_persists — items stay after page refresh",
        ],
        "pom":  "Create pages/cart_page.py with badge, item list, checkout button locators",
        "warn": "Cart badge may not exist when count is 0 — use is_visible() before reading text",
    },
    "forms": {
        "title": "Forms detected",
        "tests": [
            "test_form_valid_submission — valid data should succeed",
            "test_form_required_fields — empty required fields should error",
            "test_form_invalid_format — wrong email format should be rejected",
        ],
        "pom":  "Use get_by_label() for all form inputs — most stable locator strategy",
        "warn": "Always test both success AND failure paths for every form",
    },
    "dropdown": {
        "title": "Dropdown/select detected",
        "tests": [
            "test_sort_changes_order — selecting option reorders items",
            "test_dropdown_default_value — correct option selected on load",
        ],
        "pom":  "Use page.locator('select').select_option('value')",
        "warn": "Custom dropdowns (not <select>) need click + option click — check the HTML first",
    },
    "pagination": {
        "title": "Pagination detected",
        "tests": [
            "test_next_page — clicking next loads new results",
            "test_page_url_updates — URL reflects current page number",
        ],
        "pom":  "Add next_button, prev_button locators to your listing page POM",
        "warn": "After clicking next, use page.wait_for_load_state('networkidle')",
    },
    "tables": {
        "title": "Data table detected",
        "tests": [
            "test_table_row_count — verify expected number of rows",
            "test_table_sort_column — clicking column header sorts data",
        ],
        "pom":  "Use page.locator('table tbody tr') to count rows. Use .nth(0) for first row",
        "warn": "Tables with lazy-load need scroll before asserting row count",
    },
}


def analyse(url: str):
    print(f"\n{'='*55}")
    print(f"  ShopTest Pro — URL Analyser")
    print(f"  Scanning: {url}")
    print(f"{'='*55}\n")

    api_endpoints = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page    = context.new_page()

        page.on("request", lambda req: api_endpoints.append(req.url)
                if req.resource_type in ("fetch", "xhr") else None)

        try:
            resp   = page.goto(url, timeout=20000, wait_until="domcontentloaded")
            status = resp.status if resp else 0
        except Exception as e:
            print(f"  ERROR: Could not load URL\n  {e}\n")
            print("  Possible reasons:")
            print("  - URL is wrong or server is down")
            print("  - Site blocks automated browsers")
            print("  - Try opening it manually in Chrome first\n")
            browser.close()
            return

        page.wait_for_timeout(2000)
        title = page.title()
        print(f"  HTTP Status : {status}")
        print(f"  Page Title  : {title}")
        print(f"  Final URL   : {page.url}\n")

        if status >= 400:
            print(f"  WARNING: Server returned {status}. Fix the URL before writing tests.\n")

        found = {
            "login_form":  bool(page.query_selector("input[type='password']")),
            "search_box":  bool(page.query_selector("input[type='search'], input[placeholder*='search' i]")),
            "cart":        bool(page.query_selector("[class*='cart' i], [href*='cart' i], [data-test*='cart' i]")),
            "forms":       len(page.query_selector_all("form")) > 0,
            "dropdown":    bool(page.query_selector("select, [class*='dropdown' i]")),
            "pagination":  bool(page.query_selector("[class*='pagination' i], [aria-label*='page' i]")),
            "tables":      bool(page.query_selector("table")),
        }
        browser.close()

    detected = [k for k, v in found.items() if v]

    print("  FEATURES DETECTED")
    print("  " + "-"*40)
    if detected:
        for d in detected:
            print(f"  + {d.replace('_', ' ').title()}")
    else:
        print("  Nothing detected — page may need login first.")
        print("  Run: playwright codegen " + url)
    print()

    print("  TEST RECOMMENDATIONS")
    print("  " + "-"*40)
    for key in detected:
        if key in ADVICE:
            a = ADVICE[key]
            print(f"\n  [{a['title']}]")
            print("  Tests to write:")
            for t in a["tests"]:
                print(f"    - {t}")
            print(f"  POM advice : {a['pom']}")
            print(f"  Watch out  : {a['warn']}")

    if api_endpoints:
        print(f"\n  [API/fetch calls detected — {len(api_endpoints)} requests]")
        print("  Add API tests for these endpoints:")
        for ep in list(set(api_endpoints))[:5]:
            print(f"    {ep}")

    print(f"\n  NEXT STEPS")
    print("  " + "-"*40)
    print(f"  1. Update .env:  BASE_URL={url}")
    print(f"  2. Run:  playwright codegen {url}  (auto-records your clicks as test code)")
    print(f"  3. Update locators in pages/ folder to match this site's HTML")
    print(f"  4. Run:  pytest -v")
    print()

    os.makedirs("reports", exist_ok=True)
    with open("reports/url_analysis.json", "w") as f:
        json.dump({
            "url": url,
            "title": title,
            "detected": found,
            "api_endpoints": api_endpoints[:10],
        }, f, indent=2)
    print("  Report saved: reports/url_analysis.json\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python utils/url_analyser.py https://yourwebsite.com")
        sys.exit(1)
    analyse(sys.argv[1])
