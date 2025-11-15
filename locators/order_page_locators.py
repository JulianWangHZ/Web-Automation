from utils.locator_converter import selector


class OrderPageLocators:
    RESTAURANT_HEADING = selector('page.locator("[data-cy=\\"branch-name-order-page\\"]")')
    DELIVERY_PROMPT = selector('page.locator("[data-testid=\\"GeneralIndicator\\"]")')
    BRANCH_ADDRESS = selector('page.locator("[data-cy=\\"branch-address-order-page\\"]")')
    MENU_NAVIGATION = selector('page.locator("#category-navbar")')
    SERVICE_SWITCHER = selector('page.locator("[data-cy=\\"online-order-switch\\"]")')
    DELIVERY_SWITCHER_BUTTON = selector('page.locator("[data-cy=\\"bt-delivery\\"]")')
    TAKEOUT_SWITCHER_BUTTON = selector('page.locator("[data-cy=\\"bt-takeout\\"]")')
    ADDRESS_PICKER_TRIGGER = selector('page.locator("[data-cy=\\"go-to-address-and-date-picker\\"]")')
    ADDRESS_PICKER_MODAL = selector('page.locator("[class*=\\\"AddressTimePicker__Picker\\\"]")')
    ADDRESS_CLEAR_BUTTON = selector('page.locator("[data-cy=\\"address-clear-button\\"]")')
    ADDRESS_SEARCH_INPUT = selector('page.locator("input[placeholder=\\"Please ONLY enter the street address.\\"]")')
    ADDRESS_SUGGESTION_ITEMS = selector('page.locator("[class*=\\\"AddressTimePicker__AddressPickerBlock\\\"] li.cursor-pointer")')
    ADDRESS_CONFIRM_BUTTON = selector('page.locator("[data-cy=\\"bt-confirm-date-address\\"]")')
    DELIVERY_ADDRESS_TEXT = selector('page.locator("[data-cy=\\"delivery-address-order-page\\"]")')
    ADDRESS_EDIT_TEXT = selector('page.locator("[data-testid=\\"GeneralIndicator\\"] span[data-i18n-key=\\"takeoutOrderPage.edit\\"]")')

