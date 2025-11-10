from utils.locator_converter import selector


class OrderPageLocators:
    RESTAURANT_HEADING = selector('page.locator("[data-cy="branch-name-order-page"]")')
    DELIVERY_PROMPT = selector('page.locator("[data-testid=\\"GeneralIndicator\\"]")')
    BRANCH_ADDRESS = selector('page.locator("[data-cy=\\"branch-address-order-page\\"]")')
    MENU_NAVIGATION = selector('page.locator("#category-navbar")')

