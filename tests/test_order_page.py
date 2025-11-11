from pytest_bdd import given, scenarios, when, then, parsers  # type: ignore

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




# Scenario: Select delivery option from Delivery/Takeout switcher @successful_delivery_selection @order_page
@given("I have opened the Food Ordering page")
def have_opened_food_ordering_page(browser):
    page = OrderPage(browser)
    page.open()
    page.wait_for_page_loaded()


@then("the Delivery/Takeout switcher should be visible")
def verify_switcher_visible(browser):
    page = OrderPage(browser)
    assert page.is_switcher_button_visible(), "Delivery/Takeout switcher button is not visible."


@then("the switcher should allow me to select my desired service type")
def verify_switcher_allows_selection(browser):
    page = OrderPage(browser)
    assert page.are_switcher_options_visible(), "Switcher options are not visible."


@when(parsers.parse('I select "{option}"'))
def select_delivery_service_type(browser, option: str):
    page = OrderPage(browser)
    page.select_service_type(option)


@then("the delivery prompt message should be visible")
def verify_delivery_prompt_visible(browser):
    page = OrderPage(browser)
    assert page.is_delivery_prompt_message_visible(), "Delivery prompt message is visible after selecting Delivery."
    
    
@when(parsers.parse('I select "{option}"'))
def select_delivery_service_type(browser, option: str):
    page = OrderPage(browser)
    page.select_service_type(option)
    

@then("the delivery prompt message should not be visible")
def verify_delivery_prompt_not_visible(browser):
    page = OrderPage(browser)
    assert page.is_delivery_prompt_message_hidden(), "Delivery prompt message is still visible after selecting Takeout."
