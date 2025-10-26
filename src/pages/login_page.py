"""
Login Page Object Model for SauceDemo application.
Contains locators and methods for login functionality.
"""

from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from src.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object Model for SauceDemo Login Page"""

    # URL
    URL = "https://www.saucedemo.com/"

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_BUTTON = (By.CSS_SELECTOR, "button.error-button")
    LOGIN_LOGO = (By.CLASS_NAME, "login_logo")
    LOGIN_CREDENTIALS = (By.ID, "login_credentials")
    LOGIN_PASSWORD = (By.CLASS_NAME, "login_password")

    def __init__(self, driver: WebDriver, timeout: float = 10):
        """
        Initialize LoginPage
        
        Args:
            driver: WebDriver instance
            timeout: Default timeout for waits
        """
        super().__init__(driver, timeout)

    def navigate_to_login_page(self) -> None:
        """Navigate to the login page"""
        self.driver.get(self.URL)

    def enter_username(self, username: str) -> None:
        """
        Enter username in the username field
        
        Args:
            username: Username to enter
        """
        self.send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """
        Enter password in the password field
        
        Args:
            password: Password to enter
        """
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_login_button(self) -> None:
        """Click the login button"""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """
        Perform complete login action
        
        Args:
            username: Username to login with
            password: Password to login with
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self) -> str:
        """
        Get the error message text displayed on failed login
        
        Returns:
            str: Error message text
        """
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed
        
        Returns:
            bool: True if error message is displayed, False otherwise
        """
        return self.is_displayed(self.ERROR_MESSAGE)

    def click_error_close_button(self) -> None:
        """Click the error message close button"""
        self.click(self.ERROR_BUTTON)

    def is_login_button_displayed(self) -> bool:
        """
        Check if login button is displayed
        
        Returns:
            bool: True if login button is displayed
        """
        return self.is_displayed(self.LOGIN_BUTTON)

    def is_on_login_page(self) -> bool:
        """
        Verify if user is on the login page
        
        Returns:
            bool: True if on login page, False otherwise
        """
        return self.is_displayed(self.LOGIN_LOGO) and self.is_displayed(self.LOGIN_BUTTON)

    def get_username_placeholder(self) -> Optional[str]:
        """
        Get the placeholder text of username field
        
        Returns:
            str: Placeholder text
        """
        return self.get_attribute(self.USERNAME_INPUT, "placeholder")

    def get_password_placeholder(self) -> Optional[str]:
        """
        Get the placeholder text of password field
        
        Returns:
            str: Placeholder text
        """
        return self.get_attribute(self.PASSWORD_INPUT, "placeholder")

    def clear_username(self) -> None:
        """Clear the username input field"""
        element = self.find_element(self.USERNAME_INPUT)
        element.clear()

    def clear_password(self) -> None:
        """Clear the password input field"""
        element = self.find_element(self.PASSWORD_INPUT)
        element.clear()

    def is_username_field_enabled(self) -> bool:
        """
        Check if username field is enabled
        
        Returns:
            bool: True if enabled, False otherwise
        """
        return self.is_enabled(self.USERNAME_INPUT)

    def is_password_field_enabled(self) -> bool:
        """
        Check if password field is enabled
        
        Returns:
            bool: True if enabled, False otherwise
        """
        return self.is_enabled(self.PASSWORD_INPUT)

    def is_login_button_enabled(self) -> bool:
        """
        Check if login button is enabled
        
        Returns:
            bool: True if enabled, False otherwise
        """
        return self.is_enabled(self.LOGIN_BUTTON)

    def wait_for_login_page_to_load(self, timeout: Optional[float] = None) -> None:
        """
        Wait for login page to fully load
        
        Args:
            timeout: Maximum wait time in seconds
        """
        self.wait_for_element_visible(self.LOGIN_LOGO, timeout)
        self.wait_for_element_visible(self.LOGIN_BUTTON, timeout)

    def get_login_credentials_text(self) -> str:
        """
        Get the accepted usernames text from the login page
        
        Returns:
            str: Text containing accepted usernames
        """
        return self.get_text(self.LOGIN_CREDENTIALS)

    def get_login_password_text(self) -> str:
        """
        Get the password text from the login page
        
        Returns:
            str: Text containing password information
        """
        return self.get_text(self.LOGIN_PASSWORD)