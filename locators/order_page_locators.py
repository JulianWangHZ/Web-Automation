from utils.locator_converter import selector


class OrderPageLocators:
    RESTAURANT_HEADING = selector('page.locator("[data-cy=\\"branch-name-order-page\\"]")')
    DELIVERY_PROMPT = selector('page.locator("[data-testid=\\"GeneralIndicator\\"]")')
    BRANCH_ADDRESS = selector('page.locator("[data-cy=\\"branch-address-order-page\\"]")')
    MENU_NAVIGATION = selector('page.locator("#category-navbar")')
    SERVICE_SWITCHER = selector('page.locator("[data-cy=\\"online-order-switch\\"]")')
    DELIVERY_SWITCHER_BUTTON = selector('page.locator("[data-cy=\\"bt-delivery\\"]")')
    TAKEOUT_SWITCHER_BUTTON = selector('page.locator("[data-cy=\\"bt-takeout\\"]")')

