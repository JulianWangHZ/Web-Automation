from selenium.common.exceptions import NoSuchElementException  # type: ignore

from pages.base_actions.base_action import BaseAction
from url import BASE_URL
from locators.order_page_locators import OrderPageLocators


class OrderPage(BaseAction):
    def open(self) -> None:
        self.open_url(url=BASE_URL)

    def wait_for_page_loaded(self) -> None:
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

    def select_service_type(self, option: str) -> None:
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

