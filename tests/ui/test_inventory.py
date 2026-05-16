"""tests/ui/test_inventory.py — Products page: load, sort, add/remove cart."""

import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.fixture(autouse=True)
def login_before_each(page: Page, credentials: dict):
    LoginPage(page).navigate().login(credentials["username"], credentials["password"])
    yield


@pytest.mark.smoke
@pytest.mark.ui
def test_inventory_page_loads(page: Page):
    inventory = InventoryPage(page)
    inventory.assert_on_page()
    names = inventory.get_all_product_names()
    assert len(names) == 6, f"Expected 6 products but found {len(names)}"


@pytest.mark.ui
def test_sort_name_a_to_z(page: Page):
    inventory = InventoryPage(page)
    inventory.sort_by("az")
    names = inventory.get_all_product_names()
    assert names == sorted(names)


@pytest.mark.ui
def test_sort_name_z_to_a(page: Page):
    inventory = InventoryPage(page)
    inventory.sort_by("za")
    names = inventory.get_all_product_names()
    assert names == sorted(names, reverse=True)


@pytest.mark.ui
def test_sort_price_low_to_high(page: Page):
    inventory = InventoryPage(page)
    inventory.sort_by("lohi")
    prices = inventory.get_all_prices()
    assert prices == sorted(prices)


@pytest.mark.ui
def test_sort_price_high_to_low(page: Page):
    inventory = InventoryPage(page)
    inventory.sort_by("hilo")
    prices = inventory.get_all_prices()
    assert prices == sorted(prices, reverse=True)


@pytest.mark.smoke
@pytest.mark.ui
def test_add_single_item_to_cart(page: Page):
    InventoryPage(page).add_item_to_cart("Sauce Labs Backpack")
    InventoryPage(page).assert_cart_count(1)


@pytest.mark.ui
def test_add_multiple_items_to_cart(page: Page):
    inventory = InventoryPage(page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.add_item_to_cart("Sauce Labs Bike Light")
    inventory.add_item_to_cart("Sauce Labs Bolt T-Shirt")
    inventory.assert_cart_count(3)


@pytest.mark.ui
def test_remove_item_from_cart(page: Page):
    inventory = InventoryPage(page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.add_item_to_cart("Sauce Labs Bike Light")
    inventory.assert_cart_count(2)
    inventory.remove_item_from_cart("Sauce Labs Backpack")
    inventory.assert_cart_count(1)


@pytest.mark.ui
def test_cart_empty_after_removing_all(page: Page):
    inventory = InventoryPage(page)
    inventory.add_item_to_cart("Sauce Labs Backpack")
    inventory.remove_item_from_cart("Sauce Labs Backpack")
    inventory.assert_cart_count(0)
