import time  

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
from config.config import Config
from pages.base_actions.base_utils import BaseUtils


class BaseAction:
    def __init__(self, driver):
        self.driver = driver
        self.config = Config()
        self.wait = WebDriverWait(driver, self.config.DEFAULT_TIMEOUT)
        self.utils = BaseUtils()

    def open_url(self, url=None, path=None):
        """
        Opens the specified URL in the browser.
        
        Args:
            url: Full URL to open. If None, uses BASE_URL from config
            path: Path to append to BASE_URL, e.g. 'login' or 'products'
        """
        if url:
            target_url = url
        else:
            target_url = self.config.get_page_url(path or '')
            
        self.driver.get(target_url)
        self.driver.implicitly_wait(10)

    def find_element(self, locator_type, locator_value):
        """
        Finds the element with explicit wait and returns it
        """
        return self.wait.until(
            expected_conditions.presence_of_element_located((locator_type, locator_value))
        )

    def is_element_visible(self, locator_type, locator_value):
        """
        Checks if the element is visible and returns the boolean value
        """
        try:
            self.wait.until(
                expected_conditions.visibility_of_element_located((locator_type, locator_value))
            )
            return True
        except TimeoutException:
            return False

    def click_element(self, locator_type, locator_value):
            """
            Click on a clickable element with fallback to JavaScript click if standard click fails
            """
            try:
                # Try standard click first
                element = self.wait.until(
                    expected_conditions.element_to_be_clickable((locator_type, locator_value))
                )
                element.click()
            except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException):
                # If standard click fails, try JavaScript click
                element = self.driver.find_element(locator_type, locator_value)
                self.driver.execute_script("arguments[0].click();", element)

    def click_if_exists(self, locator_type, locator_value):
        """
        Click if element exists
        """
        if self.is_element_visible(locator_type, locator_value):
            self.click_element(locator_type, locator_value)
            return True
        return False

    def send_keys_to_element(self, locator_type, locator_value, text):
        """
        Sends keyboard input to the specified element.
        Only clear the field if it has a value.
        After clearing, verify that the field has been cleared.
        """
        element = self.find_element(locator_type, locator_value)

        # Get the current field value
        current_value = element.get_attribute('value')

        # Only clear the field if it has a value
        if current_value:
            element.clear()

            # After clearing, verify that the field has been cleared
            max_attempts = 5
            attempts = 0
            while attempts < max_attempts:
                cleared_value = element.get_attribute('value')
                if not cleared_value or cleared_value.strip() == '':
                    break  # Successfully cleared, the field is empty

                # Try to clear again
                element.clear()
                attempts += 1
                time.sleep(0.2)

            if attempts == max_attempts:
                # If the field cannot be cleared after multiple attempts, record a warning and continue
                print(f"Warning: Unable to clear field {locator_type}, {locator_value}, current value: {element.get_attribute('value')}")

        # Ensure the input is a string type
        text = str(text)
        element.send_keys(text)

    def get_element_text(self, locator_type, locator_value):
        """
        Get element text
        """
        element = self.find_element(locator_type, locator_value)
        return element.text

    def wait_for_element_visible(self, locator_type, locator_value):
        """
        Waits until the specified element becomes visible
        Raises TimeoutException with detailed error message if element not found
        """
        try:
            self.wait.until(
                expected_conditions.visibility_of_element_located((locator_type, locator_value))
            )
        except TimeoutException:
            raise TimeoutException(
                f"Element not found or not visible:\n"
                f"Locator type: {locator_type}\n"
                f"Locator value: {locator_value}\n"
            )

    def wait_for_element_clickable(self, locator_type, locator_value, timeout=10):
        """
        Waits until the specified element becomes clickable
        
        Args:
            locator_type: Type of locator (id, xpath, css_selector, etc.)
            locator_value: Value of the locator
            timeout: Maximum time to wait in seconds (default: 10)
            
        Returns:
            bool: True if element becomes clickable within timeout, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                expected_conditions.element_to_be_clickable((locator_type, locator_value))
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_not_clickable(self, locator_type, locator_value, timeout=5):
        """
        Waits until the specified element becomes not clickable (disabled or covered)
        
        Returns:
            bool: True if element becomes not clickable within timeout, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until_not(
                expected_conditions.element_to_be_clickable((locator_type, locator_value))
            )
            return True
        except TimeoutException:
            return False

    def is_element_clickable(self, locator_type, locator_value):
        """
        Checks if the element is currently clickable without waiting (immediate check)
        
        Args:
            locator_type: Type of locator (id, xpath, css_selector, etc.)
            locator_value: Value of the locator
            
        Returns:
            bool: True if element is clickable, False otherwise
        """
        try:
            element = self.driver.find_element(locator_type, locator_value)
            # Immediately check if element is enabled and displayed (no waiting)
            return element.is_enabled() and element.is_displayed()
        except Exception:
            return False

    def verify_element_not_clickable(self, locator_type, locator_value, timeout=10):
        """
        Verifies that an element is not clickable (disabled or covered)
        
        Args:
            locator_type: Type of locator (id, xpath, css_selector, etc.)
            locator_value: Value of the locator
            timeout: Maximum time to wait in seconds (default: 10)
            
        Returns:
            bool: True if element is not clickable
            
        Raises:
            AssertionError: If element is clickable when it should not be
        """
        # First check if element exists
        try:
            element = self.find_element(locator_type, locator_value)
        except TimeoutException:
            raise AssertionError(f"Element not found: {locator_type}, {locator_value}")
        
        # Wait for element to become not clickable
        if not self.wait_for_element_not_clickable(locator_type, locator_value, timeout):
            raise AssertionError(
                f"Element is still clickable in {timeout} seconds: {locator_type}, {locator_value}"
            )
        
        # Double check by verifying element is disabled or not clickable
        if element.is_enabled():
            # Element is enabled but might be covered, check if it's actually clickable
            if self.is_element_clickable(locator_type, locator_value):
                raise AssertionError(
                    f"Element exists but should not be clickable: {locator_type}, {locator_value}"
                )
        
        return True

    def wait_for_element_present(self, locator_type, locator_value, timeout=3):
        """
        Wait for the element to be present, not necessarily visible
        """
        WebDriverWait(self.driver, timeout, poll_frequency=0.1).until(
            expected_conditions.presence_of_element_located((locator_type, locator_value))
        )
        return True

    def verify_element_text(self, locator_type, locator_value, expected_text):
        actual_text = self.get_element_text(locator_type, locator_value)
        return actual_text == expected_text

    def verify_element_visible(self, locator_type, locator_value):
        return self.is_element_visible(locator_type, locator_value)

    def verify_element_clickable(self, locator_type, locator_value, timeout=10):
        """
        Verifies that an element is clickable
        
        Args:
            locator_type: Type of locator (id, xpath, css_selector, etc.)
            locator_value: Value of the locator
            timeout: Maximum time to wait in seconds (default: 10)
            
        Returns:
            bool: True if element is clickable
            
        Raises:
            AssertionError: If element is not clickable within timeout
        """
        if not self.wait_for_element_clickable(locator_type, locator_value, timeout):
            raise AssertionError(
                f"Element is not clickable in {timeout} seconds: {locator_type}, {locator_value}"
            )
        return True

    def scroll_to_element(self, locator_type, locator_value):
        """
        Scrolls the page until the specified element is visible.
        """
        element = self.find_element(locator_type, locator_value)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    def wait_for_element_disappears(self, locator_type, locator_value, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                expected_conditions.presence_of_element_located((locator_type, locator_value))
            )
            return True
        except TimeoutException:
            raise AssertionError(f"Element does not disappear in {timeout} seconds: {locator_type}, {locator_value}")

    def wait_for_element_text_contains(self, locator_type, locator_value, expected_text, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                expected_conditions.text_to_be_present_in_element(
                    (locator_type, locator_value), expected_text
                )
            )
            return True
        except TimeoutException as exc:
            raise AssertionError(
                f"Element text does not contain the expected text: {expected_text} in {timeout} seconds. "
                f"Locator: ({locator_type}, {locator_value})"
            ) from exc

    def wait_for_element_text_not_contains(self, locator_type, locator_value, unexpected_text, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until_not(
                expected_conditions.text_to_be_present_in_element(
                    (locator_type, locator_value), unexpected_text
                )
            )
            return True
        except TimeoutException as exc:
            raise AssertionError(
                f"Element text still contains the unexpected text: {unexpected_text} in {timeout} seconds. "
                f"Locator: ({locator_type}, {locator_value})"
            ) from exc

    def refresh_page(self):
        self.driver.refresh()
        self.driver.implicitly_wait(10)

    def refresh_and_wait_for_element(self, locator_type, locator_value, timeout=10):
        """
        Refresh the page and wait for the specified element to appear

        Args:
            locator_type: Locator type
            locator_value: Locator value
            timeout: Timeout in seconds
        """
        self.driver.refresh()
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            expected_conditions.visibility_of_element_located((locator_type, locator_value))
        )

    def wait_for_element_has_value(self, locator_type, locator_value, timeout=10):
        """
        Wait for the element to have a value, until the element's value attribute is not empty or timeout

        Args:
            locator_type: Locator type
            locator_value: Locator value
            timeout: Timeout in seconds

        Returns:
            bool: True if the element has a value before timeout, False otherwise

        Raises:
            TimeoutException: If the timeout is exceeded and raise_exception is True
        """
        # First ensure the element exists and is visible
        self.wait_for_element_visible(locator_type, locator_value)

        # Get the element
        element = self.find_element(locator_type, locator_value)

        # Set the timeout
        end_time = time.time() + timeout

        # Loop to check if the element has a value
        while time.time() < end_time:
            current_value = element.get_attribute('value')
            if current_value and current_value.strip():
                return True

            # Wait for a short period of time and check again
            time.sleep(0.5)

        # Timeout still no value, raise an exception
        raise TimeoutException(f"Element in {timeout} seconds did not get a value: {locator_type}, {locator_value}")
