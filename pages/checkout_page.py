"""pages/checkout_page.py — Page Object Model for the Checkout flow."""

from playwright.sync_api import Page, expect


class CheckoutPage:

    def __init__(self, page: Page):
        self.page             = page
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input  = page.get_by_placeholder("Last Name")
        self.zip_input        = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button  = page.get_by_role("button", name="Continue")
        self.error_message    = page.locator("[data-test='error']")
        self.finish_button    = page.get_by_role("button", name="Finish")
        self.summary_total    = page.locator(".summary_total_label")
        self.complete_header  = page.locator(".complete-header")

    def fill_shipping_info(self, first_name: str, last_name: str, zip_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.zip_input.fill(zip_code)
        self.continue_button.click()
        return self

    def complete_order(self):
        self.finish_button.click()
        return self

    def get_order_total(self) -> str:
        return self.summary_total.inner_text()

    def assert_order_complete(self):
        expect(self.complete_header).to_have_text("Thank you for your order!")

    def assert_error_visible(self, text: str):
        expect(self.error_message).to_contain_text(text)
