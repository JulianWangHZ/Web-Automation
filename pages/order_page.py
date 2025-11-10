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

