"""tests/ui/test_login.py — Login tests: valid, invalid, parametrized, logout."""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
@pytest.mark.ui
def test_valid_login(page: Page, credentials: dict):
    login = LoginPage(page).navigate()
    login.login(credentials["username"], credentials["password"])
    login.assert_logged_in()
    InventoryPage(page).assert_on_page()


@pytest.mark.ui
def test_locked_out_user(page: Page, credentials: dict):
    LoginPage(page).navigate().login(credentials["locked_user"], credentials["password"])
    LoginPage(page).assert_error_visible("Sorry, this user has been locked out")


@pytest.mark.ui
def test_empty_credentials(page: Page):
    LoginPage(page).navigate().login("", "")
    LoginPage(page).assert_error_visible("Username is required")


@pytest.mark.ui
def test_empty_password(page: Page, credentials: dict):
    LoginPage(page).navigate().login(credentials["username"], "")
    LoginPage(page).assert_error_visible("Password is required")


@pytest.mark.ui
@pytest.mark.parametrize("username, password, expected_error", [
    ("wrong_user",    "secret_sauce", "Username and password do not match"),
    ("standard_user", "wrong_pass",   "Username and password do not match"),
    ("",              "secret_sauce", "Username is required"),
])
def test_invalid_login_combinations(page: Page, username, password, expected_error):
    LoginPage(page).navigate().login(username, password)
    LoginPage(page).assert_error_visible(expected_error)


@pytest.mark.smoke
@pytest.mark.ui
def test_logout(page: Page, credentials: dict):
    LoginPage(page).navigate().login(credentials["username"], credentials["password"])
    LoginPage(page).assert_logged_in()
    InventoryPage(page).logout()
    expect(page).to_have_url("https://www.saucedemo.com/")
