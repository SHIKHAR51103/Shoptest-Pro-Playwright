"""tests/ui/test_checkout.py — Full E2E checkout flow tests."""

import pytest
from faker import Faker
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

fake = Faker("en_IN")


@pytest.fixture(autouse=True)
def login_before_each(page: Page, credentials: dict):
    LoginPage(page).navigate().login(credentials["username"], credentials["password"])
    yield


@pytest.mark.smoke
@pytest.mark.ui
def test_complete_purchase_single_item(page: Page):
    InventoryPage(page).add_item_to_cart("Sauce Labs Backpack")
    InventoryPage(page).go_to_cart()
    CartPage(page).assert_on_page()
    CartPage(page).assert_item_present("Sauce Labs Backpack")
    CartPage(page).assert_item_count(1)
    CartPage(page).proceed_to_checkout()
    CheckoutPage(page).fill_shipping_info(fake.first_name(), fake.last_name(), fake.postcode())
    CheckoutPage(page).complete_order()
    CheckoutPage(page).assert_order_complete()


@pytest.mark.ui
def test_complete_purchase_multiple_items(page: Page):
    inventory = InventoryPage(page)
    for item in ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]:
        inventory.add_item_to_cart(item)
    inventory.assert_cart_count(3)
    inventory.go_to_cart()
    CartPage(page).assert_item_count(3)
    CartPage(page).proceed_to_checkout()
    CheckoutPage(page).fill_shipping_info("Rahul", "Sharma", "110001")
    CheckoutPage(page).complete_order()
    CheckoutPage(page).assert_order_complete()


@pytest.mark.ui
def test_checkout_missing_first_name(page: Page):
    InventoryPage(page).add_item_to_cart("Sauce Labs Backpack")
    InventoryPage(page).go_to_cart()
    CartPage(page).proceed_to_checkout()
    CheckoutPage(page).fill_shipping_info("", "Sharma", "110001")
    CheckoutPage(page).assert_error_visible("First Name is required")


@pytest.mark.ui
def test_checkout_missing_last_name(page: Page):
    InventoryPage(page).add_item_to_cart("Sauce Labs Backpack")
    InventoryPage(page).go_to_cart()
    CartPage(page).proceed_to_checkout()
    CheckoutPage(page).fill_shipping_info("Rahul", "", "110001")
    CheckoutPage(page).assert_error_visible("Last Name is required")


@pytest.mark.ui
def test_checkout_missing_zip(page: Page):
    InventoryPage(page).add_item_to_cart("Sauce Labs Backpack")
    InventoryPage(page).go_to_cart()
    CartPage(page).proceed_to_checkout()
    CheckoutPage(page).fill_shipping_info("Rahul", "Sharma", "")
    CheckoutPage(page).assert_error_visible("Postal Code is required")


@pytest.mark.ui
@pytest.mark.parametrize("first, last, zip_code", [
    ("Amit",   "Kumar", "400001"),
    ("Priya",  "Verma", "600001"),
    ("Vikram", "Singh", "700001"),
])
def test_checkout_various_shipping_info(page: Page, first, last, zip_code):
    InventoryPage(page).add_item_to_cart("Sauce Labs Bolt T-Shirt")
    InventoryPage(page).go_to_cart()
    CartPage(page).proceed_to_checkout()
    CheckoutPage(page).fill_shipping_info(first, last, zip_code)
    CheckoutPage(page).complete_order()
    CheckoutPage(page).assert_order_complete()
