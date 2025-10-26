"""
Base Page class containing common methods for all page objects.
All page classes will inherit from this base class.
"""

from typing import Optional, Tuple, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.select import Select
from typing import Union

class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver: WebDriver, timeout: float = 10):
        """
        Initialize BasePage with WebDriver instance
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for waits (default: 10 seconds)
        """
        self.driver = driver
        self.timeout = timeout
        self.driver.implicitly_wait(timeout)  # Set implicit wait globally
        self.wait = WebDriverWait(driver, timeout)
        self.actions = ActionChains(driver)

    def find_element(self, locator: Tuple, timeout: Optional[float] = None) -> WebElement:
        """
        Find a single element with explicit wait
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time in seconds (uses instance timeout if None)
            
        Returns:
            WebElement: Found element
        """
        timeout = timeout if timeout is not None else self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not found within {timeout} seconds")

    def find_elements(self, locator: Tuple, timeout: Optional[float] = None) -> List[WebElement]:
        """
        Find multiple elements with explicit wait
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time in seconds (uses instance timeout if None)
            
        Returns:
            List[WebElement]: List of found elements
        """
        timeout = timeout if timeout is not None else self.timeout
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            raise TimeoutException(f"Elements {locator} not found within {timeout} seconds")

    def click(self, locator: Tuple, timeout: Optional[float] = None) -> None:
        """
        Click on an element with interactability checks
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time in seconds
        """
        from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
        
        timeout = timeout if timeout is not None else self.timeout
        
        try:
            # Wait for page to be interactive
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for element to be clickable
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            
            # Ensure element is in viewport
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", 
                element
            )
            
            # Small wait for any scroll animations
            WebDriverWait(self.driver, 2).until(
                lambda d: d.execute_script(
                    "return arguments[0].getBoundingClientRect().top >= 0 && "
                    "arguments[0].getBoundingClientRect().top <= window.innerHeight", 
                    element
                )
            )
            
            # Try standard click
            try:
                element.click()
            except (ElementClickInterceptedException, StaleElementReferenceException):
                # Fallback to JavaScript click
                element = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].click();", element)
                
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable within {timeout} seconds")

    def send_keys(self, locator: Tuple, text: str, timeout: Optional[float] = None) -> None:
        """
        Send keys to an element
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            text: Text to send to element
            timeout: Maximum wait time in seconds
        """
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple, timeout: Optional[float] = None) -> str:
        """
        Get text from an element
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time in seconds
            
        Returns:
            str: Text content of the element
        """
        element = self.find_element(locator, timeout)
        return element.text

    def get_attribute(self, locator, attribute_name, timeout=None):
        """
        Get attribute value from an element
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            attribute_name: Name of the attribute
            timeout: Maximum wait time in seconds
            
        Returns:
            str: Attribute value
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute_name)

    def is_displayed(self, locator, timeout=None):
        """
        Check if element is displayed
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time in seconds
            
        Returns:
            bool: True if element is displayed, False otherwise
        """
        try:
            element = self.find_element(locator, timeout)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_enabled(self, locator, timeout=None):
        """
        Check if element is enabled
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time in seconds
            
        Returns:
            bool: True if element is enabled, False otherwise
        """
        try:
            element = self.find_element(locator, timeout)
            return element.is_enabled()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_element_visible(self, locator: Tuple, timeout: Optional[float] = None) -> WebElement:
        """
        Wait for element to be visible
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement: Visible element
        """
        timeout = timeout if timeout is not None else self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not visible within {timeout} seconds")

    def wait_for_element_invisible(self, locator: Tuple, timeout: Optional[float] = None) -> Union[bool, WebElement]:
        """
        Wait for element to be invisible
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time in seconds
            
        Returns:
            bool | WebElement: True if element becomes invisible, or the element if it becomes stale
        """
        timeout = timeout if timeout is not None else self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} still visible after {timeout} seconds")

    def wait_for_url_contains(self, url_fragment: str, timeout: Optional[float] = None) -> bool:
        """
        Wait for URL to contain specific text
        
        Args:
            url_fragment: Text that should be in URL
            timeout: Maximum wait time in seconds
            
        Returns:
            bool: True if URL contains the fragment
        """
        timeout = timeout if timeout is not None else self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.url_contains(url_fragment)
            )
        except TimeoutException:
            raise TimeoutException(f"URL does not contain '{url_fragment}' within {timeout} seconds")

    def wait_for_url_to_be(self, url: str, timeout: Optional[float] = None) -> bool:
        """
        Wait for URL to be exactly as specified
        
        Args:
            url: Expected URL
            timeout: Maximum wait time in seconds
            
        Returns:
            bool: True if URL matches
        """
        timeout = timeout if timeout is not None else self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.url_to_be(url)
            )
        except TimeoutException:
            raise TimeoutException(f"URL is not '{url}' within {timeout} seconds")

    def select_dropdown_by_text(self, locator, text, timeout=None):
        """
        Select dropdown option by visible text
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            text: Visible text of option to select
            timeout: Maximum wait time in seconds
        """
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)

    def select_dropdown_by_value(self, locator, value, timeout=None):
        """
        Select dropdown option by value attribute
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            value: Value attribute of option to select
            timeout: Maximum wait time in seconds
        """
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_value(value)

    def select_dropdown_by_index(self, locator, index, timeout=None):
        """
        Select dropdown option by index
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            index: Index of option to select (0-based)
            timeout: Maximum wait time in seconds
        """
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_index(index)

    def hover_over_element(self, locator, timeout=None):
        """
        Hover over an element
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time in seconds
        """
        element = self.find_element(locator, timeout)
        self.actions.move_to_element(element).perform()

    def scroll_to_element(self, locator, timeout=None):
        """
        Scroll to an element
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time in seconds
        """
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def switch_to_frame(self, locator: Tuple, timeout: Optional[float] = None) -> None:
        """
        Switch to an iframe
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value") or frame index
            timeout: Maximum wait time in seconds
        """
        timeout = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Frame {locator} not available within {timeout} seconds")

    def switch_to_default_content(self):
        """Switch back to default content from iframe"""
        self.driver.switch_to.default_content()

    def get_current_url(self):
        """
        Get current page URL
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url

    def get_page_title(self):
        """
        Get current page title
        
        Returns:
            str: Page title
        """
        return self.driver.title

    def refresh_page(self):
        """Refresh the current page"""
        self.driver.refresh()

    def navigate_back(self):
        """Navigate back in browser history"""
        self.driver.back()

    def navigate_forward(self):
        """Navigate forward in browser history"""
        self.driver.forward()

    def accept_alert(self, timeout: Optional[float] = None) -> None:
        """
        Accept JavaScript alert
        
        Args:
            timeout: Maximum wait time in seconds
        """
        timeout = timeout if timeout is not None else self.timeout
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert.accept()
        except TimeoutException:
            raise TimeoutException(f"Alert not present within {timeout} seconds")

    def dismiss_alert(self, timeout: Optional[float] = None) -> None:
        """
        Dismiss JavaScript alert
        
        Args:
            timeout: Maximum wait time in seconds
        """
        timeout = timeout if timeout is not None else self.timeout
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert.dismiss()
        except TimeoutException:
            raise TimeoutException(f"Alert not present within {timeout} seconds")

    def get_alert_text(self, timeout: Optional[float] = None) -> str:
        """
        Get text from JavaScript alert
        
        Args:
            timeout: Maximum wait time in seconds
            
        Returns:
            str: Alert text
        """
        timeout = timeout if timeout is not None else self.timeout
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            return alert.text
        except TimeoutException:
            raise TimeoutException(f"Alert not present within {timeout} seconds")

    def take_screenshot(self, filepath):
        """
        Take screenshot and save to file
        
        Args:
            filepath: Path where screenshot should be saved
        """
        self.driver.save_screenshot(filepath)