from selenium.webdriver.common.by import By

def convert_playwright_to_selenium(locator_str: str) -> tuple:
    """
    Convert Playwright locator to Selenium locator format
    
    Args:
        locator_str (str): Playwright locator string, e.g. 'page.locator('[data-sentry-component="HeaderAvatar"]')'
        
    Returns:
        tuple: Selenium locator tuple (By.CSS_SELECTOR, selector)
    """
    return selector(locator_str)

def _extract_test_id(selector_str: str) -> str:
    """Extract test ID and clean quotes"""
    test_id = selector_str.replace('page.get_by_test_id(', '').replace(')', '')
    return _clean_quotes(test_id)

def _clean_quotes(text: str) -> str:
    """Clean quotes around the string"""
    if text.startswith(('`', '"', "'")):
        return text[1:-1]  # remove quotes
    return text

def _clean_escaped_quotes(text: str) -> str:
    """Clean escaped quotes"""
    return text.replace('\\"', "'")

def _process_page_locator(selector_str: str) -> str:
    """Process page.locator selector"""
    # Extract selector part
    prefix = 'page.locator('
    selector_body = selector_str[len(prefix):]
    if selector_body.endswith(')'):
        selector_body = selector_body[:-1]
    
    # Process .first method
    if '.first' in selector_body:
        selector_body = selector_body.split('.first')[0]
        
    # Process .nth() method
    if '.nth(' in selector_body:
        selector_body = selector_body.split('.nth(')[0]
        
    return _clean_quotes(selector_body)

def _get_selenium_locator(selector_str: str) -> tuple:
    """Return corresponding Selenium locator based on selector type"""
    if selector_str.startswith('//'):
        return By.XPATH, selector_str
    elif selector_str.startswith('#'):
        return By.ID, selector_str[1:]
    elif selector_str.startswith('.'):
        return By.CLASS_NAME, selector_str[1:]
    else:
        # For CSS selectors, clean escaped quotes
        selector_str = _clean_escaped_quotes(selector_str)
        return By.CSS_SELECTOR, selector_str

def selector(selector_str: str) -> tuple:
    """
    Simplified locator conversion function, supports full Playwright format
    
    Args:
        selector_str (str): Selector string, supports the following formats:
            - Full format: 'page.locator('[data-sentry-component="HeaderAvatar"]')'
            - Full format: 'page.locator("[data-sentry-component=\"HeaderAvatar\"]")'
            - Full format: 'page.locator(`[data-sentry-component="HeaderAvatar"]`)'
            - Full format: 'page.get_by_test_id('component-id')'
            - Simplified format: '[data-sentry-component="HeaderAvatar"]'
        
    Returns:
        tuple: Selenium locator tuple
    """
    # Process page.get_by_test_id format
    if selector_str.startswith('page.get_by_test_id'):
        test_id = _extract_test_id(selector_str)
        return By.CSS_SELECTOR, f'[data-testid="{test_id}"]'

    # Process page.locator format
    if selector_str.startswith('page.locator'):
        selector_str = _process_page_locator(selector_str)
    
    return _get_selenium_locator(selector_str)


if __name__ == "__main__":
    test_locator = 'page.locator(`[data-sentry-component="HeaderAvatar"]`)'
    selenium_locator = convert_playwright_to_selenium(test_locator)