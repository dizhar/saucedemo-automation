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

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    LOGIN_LOGO = (By.CLASS_NAME, "login_logo")

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
        self.driver.get(self.base_url)

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

    # def click_error_close_button(self) -> None:
    #     """Click the error message close button"""
    #     self.click(self.ERROR_BUTTON)

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

    def wait_for_login_page_to_load(self, timeout: Optional[float] = None) -> None:
        """
        Wait for login page to fully load
        
        Args:
            timeout: Maximum wait time in seconds
        """
        self.wait_for_element_visible(self.LOGIN_LOGO, timeout)
        self.wait_for_element_visible(self.LOGIN_BUTTON, timeout)