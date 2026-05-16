"""pages/login_page.py — Page Object Model for the Login page."""

from playwright.sync_api import Page, expect


class LoginPage:
    URL = "https://www.saucedemo.com"

    def __init__(self, page: Page):
        self.page           = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button   = page.get_by_role("button", name="Login")
        self.error_message  = page.locator("[data-test='error']")

    def navigate(self):
        self.page.goto(self.URL)
        return self

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self

    def get_error_message(self) -> str:
        return self.error_message.inner_text()

    def assert_logged_in(self):
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")

    def assert_error_visible(self, expected_text: str = None):
        expect(self.error_message).to_be_visible()
        if expected_text:
            expect(self.error_message).to_contain_text(expected_text)
