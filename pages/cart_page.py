"""pages/cart_page.py — Page Object Model for the Cart page."""

from playwright.sync_api import Page, expect


class CartPage:

    def __init__(self, page: Page):
        self.page            = page
        self.title           = page.locator(".title")
        self.cart_items      = page.locator(".cart_item")
        self.item_names      = page.locator(".inventory_item_name")
        self.checkout_button = page.get_by_role("button", name="Checkout")

    def proceed_to_checkout(self):
        self.checkout_button.click()
        return self

    def get_item_names(self) -> list:
        return self.item_names.all_inner_texts()

    def assert_on_page(self):
        expect(self.title).to_have_text("Your Cart")

    def assert_item_present(self, item_name: str):
        expect(self.page.locator(".cart_item").filter(has_text=item_name)).to_be_visible()

    def assert_item_count(self, expected: int):
        expect(self.cart_items).to_have_count(expected)
