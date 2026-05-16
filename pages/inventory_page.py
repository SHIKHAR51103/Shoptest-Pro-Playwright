"""pages/inventory_page.py — Page Object Model for the Products page."""

from playwright.sync_api import Page, expect


class InventoryPage:

    def __init__(self, page: Page):
        self.page           = page
        self.title          = page.locator(".title")
        self.sort_dropdown  = page.locator("[data-test='product-sort-container']")
        self.product_names  = page.locator(".inventory_item_name")
        self.product_prices = page.locator(".inventory_item_price")
        self.cart_badge     = page.locator(".shopping_cart_badge")
        self.cart_icon      = page.locator(".shopping_cart_link")
        self.burger_menu    = page.get_by_role("button", name="Open Menu")
        self.logout_link    = page.get_by_role("link", name="Logout")

    def sort_by(self, option: str):
        self.sort_dropdown.select_option(option)
        return self

    def add_item_to_cart(self, item_name: str):
        item = self.page.locator(".inventory_item").filter(has_text=item_name)
        item.get_by_role("button", name="Add to cart").click()
        return self

    def remove_item_from_cart(self, item_name: str):
        item = self.page.locator(".inventory_item").filter(has_text=item_name)
        item.get_by_role("button", name="Remove").click()
        return self

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def go_to_cart(self):
        self.cart_icon.click()
        return self

    def logout(self):
        self.burger_menu.click()
        self.logout_link.click()

    def get_all_product_names(self) -> list:
        return self.product_names.all_inner_texts()

    def get_all_prices(self) -> list:
        raw = self.product_prices.all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def assert_on_page(self):
        expect(self.title).to_have_text("Products")

    def assert_cart_count(self, expected: int):
        if expected == 0:
            expect(self.cart_badge).not_to_be_visible()
        else:
            expect(self.cart_badge).to_have_text(str(expected))
