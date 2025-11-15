from selenium.common.exceptions import NoSuchElementException  # type: ignore

from pages.base_actions.base_action import BaseAction
from url import BASE_URL
from locators.order_page_locators import OrderPageLocators


class OrderPage(BaseAction):
    def open(self):
        self.open_url(url=BASE_URL)

    def wait_for_page_loaded(self):
        self.wait_for_element_visible(*OrderPageLocators.RESTAURANT_HEADING)
        self.wait_for_element_visible(*OrderPageLocators.DELIVERY_PROMPT)
        self.wait_for_element_visible(*OrderPageLocators.MENU_NAVIGATION)

    def get_restaurant_name(self) -> str:
        return self.get_element_text(*OrderPageLocators.RESTAURANT_HEADING)

    def is_delivery_prompt_visible(self) -> bool:
        return self.is_element_visible(*OrderPageLocators.DELIVERY_PROMPT)

    def is_menu_navigation_visible(self) -> bool:
        return self.is_element_visible(*OrderPageLocators.MENU_NAVIGATION)

    def get_branch_address_text(self) -> str:
        return self.get_element_text(*OrderPageLocators.BRANCH_ADDRESS)

    def get_delivery_prompt_text(self) -> str:
        return self.get_element_text(*OrderPageLocators.DELIVERY_PROMPT)

    def is_delivery_prompt_message_visible(self) -> bool:
        try:
            self.wait_for_element_text_contains(
                *OrderPageLocators.DELIVERY_PROMPT,
                expected_text="Please enter your delivery address.",
                timeout=5,
            )
            return True
        except AssertionError:
            return False

    def is_delivery_prompt_message_hidden(self) -> bool:
        try:
            self.wait_for_element_text_not_contains(
                *OrderPageLocators.DELIVERY_PROMPT,
                unexpected_text="Please enter your delivery address.",
                timeout=5,
            )
            return True
        except AssertionError:
            return False

    def is_switcher_button_visible(self) -> bool:
        return self.is_element_visible(*OrderPageLocators.SERVICE_SWITCHER)

    def are_switcher_options_visible(self) -> bool:
        return (
            self.is_element_visible(*OrderPageLocators.DELIVERY_SWITCHER_BUTTON)
            and self.is_element_visible(*OrderPageLocators.TAKEOUT_SWITCHER_BUTTON)
        )

    def select_service_type(self, option: str):
        normalized_option = option.strip().lower()
        if normalized_option == "delivery":
            self.click_element(*OrderPageLocators.DELIVERY_SWITCHER_BUTTON)
            self.wait_for_element_text_contains(
                *OrderPageLocators.DELIVERY_PROMPT,
                expected_text="Please enter your delivery address.",
            )
        elif normalized_option == "takeout":
            self.click_element(*OrderPageLocators.TAKEOUT_SWITCHER_BUTTON)
            self.wait_for_element_text_not_contains(
                *OrderPageLocators.DELIVERY_PROMPT,
                unexpected_text="Please enter your delivery address.",
            )
        else:
            raise ValueError(f"Unsupported service type: {option}")

    def is_delivery_option_selected(self) -> bool:
        try:
            element = self.driver.find_element(*OrderPageLocators.DELIVERY_SWITCHER_BUTTON)
        except NoSuchElementException:
            return False
        classes = element.get_attribute("class") or ""
        return "border-orange" in classes or "shadow-xl" in classes

    def open_address_picker(self):
        self.wait_for_element_clickable(*OrderPageLocators.ADDRESS_PICKER_TRIGGER)
        self.click_element(*OrderPageLocators.ADDRESS_PICKER_TRIGGER)
        self.wait_for_element_visible(*OrderPageLocators.ADDRESS_PICKER_MODAL)

    def input_postal_code(self, postal_code: str):
        self.wait_for_element_visible(*OrderPageLocators.ADDRESS_SEARCH_INPUT)
        self.send_keys_to_element(*OrderPageLocators.ADDRESS_SEARCH_INPUT, postal_code)

    def wait_for_postal_code_results(self):
        self.wait_for_element_visible(*OrderPageLocators.ADDRESS_SUGGESTION_ITEMS)

    def select_first_address_suggestion(self):
        suggestions = self.driver.find_elements(*OrderPageLocators.ADDRESS_SUGGESTION_ITEMS)
        if not suggestions:
            raise AssertionError("No address suggestions are available to select.")
        suggestions[0].click()

    def get_first_address_suggestion_text(self):
        suggestions = self.driver.find_elements(*OrderPageLocators.ADDRESS_SUGGESTION_ITEMS)
        if not suggestions:
            raise AssertionError("No address suggestions are available to read.")
        return suggestions[0].text.strip()

    def confirm_selected_address(self):
        self.wait_for_element_clickable(*OrderPageLocators.ADDRESS_CONFIRM_BUTTON)
        self.click_element(*OrderPageLocators.ADDRESS_CONFIRM_BUTTON)
        self.wait_for_element_disappears(*OrderPageLocators.ADDRESS_PICKER_MODAL)

    def get_current_delivery_address(self):
        return self.get_element_text(*OrderPageLocators.DELIVERY_ADDRESS_TEXT)

    def is_address_edit_option_visible(self):
        return self.is_element_visible(*OrderPageLocators.ADDRESS_EDIT_TEXT)

