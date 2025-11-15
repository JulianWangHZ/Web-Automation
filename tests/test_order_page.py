import pytest
from pytest_bdd import given, scenarios, when, then, parsers  # type: ignore

from pages.order_page import OrderPage


scenarios("../features/order_page.feature")


@pytest.fixture
def order_context():
    """
    Simple scenario-level context for sharing state across steps.
    """
    return {}


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





# Scenario: Input postal code and confirm delivery address @successful_postal_code_confirmation @order_page
@given(parsers.parse('I have selected "{option}" option'))
def have_selected_service_option(browser, option: str):
    page = OrderPage(browser)
    page.open()
    page.wait_for_page_loaded()
    page.select_service_type(option)


@when("I click edit button at address picker")
def click_edit_button_at_address_picker(browser):
    page = OrderPage(browser)
    page.open_address_picker()


@when(parsers.parse('I input postal code "{postal_code}" at address picker'))
def input_postal_code_at_address_picker(browser, postal_code: str, order_context):
    page = OrderPage(browser)
    page.input_postal_code(postal_code)
    page.wait_for_postal_code_results()
    order_context["postal_code"] = postal_code
    order_context["suggestion_text"] = page.get_first_address_suggestion_text()


@then("the system should use the postal code to locate the place")
def verify_postal_code_lookup_success(order_context):
    suggestion_text = order_context.get("suggestion_text", "")
    assert order_context["postal_code"] in suggestion_text, "Postal code did not return any matching suggestion."


@when("I select the searched address and confirm address")
def select_searched_address_and_confirm(browser, order_context):
    page = OrderPage(browser)
    # Use the current first suggestion for selection to ensure we click the same node text
    order_context["selected_address_text"] = page.get_first_address_suggestion_text()
    page.select_first_address_suggestion()
    page.confirm_selected_address()


@then("I should be able to successfully select and confirm the address")
def verify_address_confirmed(browser, order_context):
    page = OrderPage(browser)
    current_address = page.get_current_delivery_address()
    order_context["confirmed_address"] = current_address
    assert order_context["selected_address_text"] in current_address or order_context["postal_code"] in current_address, (
        "The confirmed delivery address does not match the selected suggestion."
    )


@then("the interface should reflect the chosen delivery address")
def verify_interface_reflects_address(order_context):
    current_address = order_context.get("confirmed_address", "")
    assert current_address and "Please enter your delivery address." not in current_address, (
        "The interface did not update with the confirmed delivery address."
    )


@then('an "Edit" option should be provided after confirming the address')
def verify_edit_option_visible(browser):
    page = OrderPage(browser)
    assert page.is_address_edit_option_visible(), "Edit option is not visible on the delivery address card."
