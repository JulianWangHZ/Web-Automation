from pytest_bdd import given, scenarios,when, then, parsers

from pages.order_page import OrderPage


scenarios("../features/order_page.feature")


# Scenario: Open Food Ordering company page @successful_order_page_load @order_page
@given("I open the Food Ordering company page")
def open_food_ordering_page(browser):
    page = OrderPage(browser)
    page.open()
    page.wait_for_page_loaded()


@then("the page should load successfully")
def verify_order_page_loaded(browser):
    page = OrderPage(browser)
    page.wait_for_page_loaded()


@then("the page should display the company's food ordering options and relevant information")
def verify_order_page_content(browser):
    page = OrderPage(browser)
    assert page.get_restaurant_name().strip(), "Restaurant name heading is empty."
    assert page.is_delivery_prompt_visible(), "Delivery prompt card is not visible."
    assert page.is_menu_navigation_visible(), "Menu navigation is not visible."
    assert page.get_branch_address_text().strip(), "Branch address text is empty."
    
