"""
Products Page Object Model for SauceDemo application.
Contains locators and methods for the products/inventory page functionality.
"""

from typing import Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from src.pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.logger import logger


class ProductsPage(BasePage):
    """Page Object Model for SauceDemo Products/Inventory Page"""

    # URL
    URL = "https://www.saucedemo.com/inventory.html"

    # Header Locators
    APP_LOGO = (By.CLASS_NAME, "app_logo")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    
    # Menu Locators
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    MENU_CLOSE_BUTTON = (By.ID, "react-burger-cross-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    ALL_ITEMS_LINK = (By.ID, "inventory_sidebar_link")
    ABOUT_LINK = (By.ID, "about_sidebar_link")
    RESET_APP_LINK = (By.ID, "reset_sidebar_link")
    
    # Product Sorting
    PRODUCT_SORT_CONTAINER = (By.CLASS_NAME, "product_sort_container")
    
    # Product Container
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    
    # Product Item Elements
    INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    INVENTORY_ITEM_DESC = (By.CLASS_NAME, "inventory_item_desc")
    INVENTORY_ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    INVENTORY_ITEM_IMG = (By.CLASS_NAME, "inventory_item_img")
    
    # Add to Cart Buttons
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_TO_CART_BIKE_LIGHT = (By.ID, "add-to-cart-sauce-labs-bike-light")
    ADD_TO_CART_BOLT_TSHIRT = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    ADD_TO_CART_FLEECE_JACKET = (By.ID, "add-to-cart-sauce-labs-fleece-jacket")
    ADD_TO_CART_ONESIE = (By.ID, "add-to-cart-sauce-labs-onesie")
    ADD_TO_CART_TSHIRT_RED = (By.ID, "add-to-cart-test.allthethings()-t-shirt-(red)")
    
    # Remove Buttons
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    REMOVE_BIKE_LIGHT = (By.ID, "remove-sauce-labs-bike-light")
    REMOVE_BOLT_TSHIRT = (By.ID, "remove-sauce-labs-bolt-t-shirt")
    REMOVE_FLEECE_JACKET = (By.ID, "remove-sauce-labs-fleece-jacket")
    REMOVE_ONESIE = (By.ID, "remove-sauce-labs-onesie")
    REMOVE_TSHIRT_RED = (By.ID, "remove-test.allthethings()-t-shirt-(red)")
    
    # Footer
    FOOTER = (By.CLASS_NAME, "footer")
    SOCIAL_TWITTER = (By.CSS_SELECTOR, "a[data-test='social-twitter']")
    SOCIAL_FACEBOOK = (By.CSS_SELECTOR, "a[data-test='social-facebook']")
    SOCIAL_LINKEDIN = (By.CSS_SELECTOR, "a[data-test='social-linkedin']")

    def __init__(self, driver: WebDriver, timeout: float = 10):
        """
        Initialize ProductsPage
        
        Args:
            driver: WebDriver instance
            timeout: Default timeout for waits
        """
        super().__init__(driver, timeout)

    def is_on_products_page(self) -> bool:
        """
        Verify if user is on the products page
        
        Returns:
            bool: True if on products page, False otherwise
        """
        
        return self.is_displayed(self.APP_LOGO) and self.is_displayed(self.INVENTORY_CONTAINER)

    def wait_for_products_page_to_load(self, timeout: Optional[float] = None) -> None:
        """
        Wait for products page to fully load
        
        Args:
            timeout: Maximum wait time in seconds
        """
        self.wait_for_element_visible(self.INVENTORY_CONTAINER, timeout)
        self.wait_for_element_visible(self.APP_LOGO, timeout)

    def get_page_title(self) -> str:
        """
        Get the page title from app logo
        
        Returns:
            str: Page title text
        """
        return self.get_text(self.APP_LOGO)

    # Shopping Cart Methods
    def click_shopping_cart(self) -> None:
        """Click the shopping cart icon"""
        self.click(self.SHOPPING_CART_LINK)

    def get_cart_badge_count(self) -> str:
        """
        Get the number displayed in the shopping cart badge
        
        Returns:
            str: Number of items in cart
        """
        return self.get_text(self.SHOPPING_CART_BADGE)

    def is_cart_badge_displayed(self) -> bool:
        """
        Check if cart badge is displayed (only shows when items are in cart)
        
        Returns:
            bool: True if badge is displayed
        """
        return self.is_displayed(self.SHOPPING_CART_BADGE)

    # Menu Methods
    def open_menu(self) -> None:
        """Open the hamburger menu and wait for it to fully open"""
        try:
            # First, check if menu is already open
            menu_wrap_locator = (By.CLASS_NAME, "bm-menu-wrap")
            menu_wrap = self.driver.find_element(*menu_wrap_locator)
            is_already_open = menu_wrap.get_attribute("aria-hidden") == "false"
            
            if is_already_open:
                logger.info("Menu is already open, skipping click")
                return
            
            logger.info("Menu is closed, opening it...")
            
            # Click menu button to open it
            menu_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.MENU_BUTTON)
            )
            menu_button.click()
            logger.info("Clicked menu button")
            
            # Wait for menu to fully open (aria-hidden changes to "false")
            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(*menu_wrap_locator).get_attribute("aria-hidden") == "false"
            )
            
            logger.info("Menu fully opened and verified")
            
        except Exception as e:
            logger.error(f"Failed to open menu: {str(e)}")
            self.driver.save_screenshot("debug_menu_open_failed.png")
            raise

    def close_menu(self) -> None:
        """Close the hamburger menu"""
        self.click(self.MENU_CLOSE_BUTTON)

    def click_logout(self) -> None:
        """Click logout from the menu"""
        self.open_menu()
        self.click(self.LOGOUT_LINK)

    def click_all_items(self) -> None:
        """Click All Items link from the menu"""
        self.click(self.ALL_ITEMS_LINK)

    def click_about(self) -> None:
        """Click About link from the menu"""
        self.click(self.ABOUT_LINK)

    def click_reset_app_state(self) -> None:
        """Click Reset App State from the menu"""
        self.click(self.RESET_APP_LINK)

    # Product Sorting Methods
    def select_sort_option(self, option: str) -> None:
        """
        Select a sorting option from the dropdown
        
        Args:
            option: Sort option text (e.g., "Name (A to Z)", "Price (low to high)")
        """
        self.select_dropdown_by_text(self.PRODUCT_SORT_CONTAINER, option)

    def select_sort_by_value(self, value: str) -> None:
        """
        Select a sorting option by value
        
        Args:
            value: Sort option value (e.g., "az", "za", "lohi", "hilo")
        """
        self.select_dropdown_by_value(self.PRODUCT_SORT_CONTAINER, value)

    # Product Methods
    def get_all_product_names(self) -> List[str]:
        """
        Get all product names displayed on the page
        
        Returns:
            List[str]: List of product names
        """
        elements = self.find_elements(self.INVENTORY_ITEM_NAME)
        return [element.text for element in elements]

    def get_all_product_prices(self) -> List[str]:
        """
        Get all product prices displayed on the page
        
        Returns:
            List[str]: List of product prices
        """
        elements = self.find_elements(self.INVENTORY_ITEM_PRICE)
        return [element.text for element in elements]

    def get_all_product_descriptions(self) -> List[str]:
        """
        Get all product descriptions displayed on the page
        
        Returns:
            List[str]: List of product descriptions
        """
        elements = self.find_elements(self.INVENTORY_ITEM_DESC)
        return [element.text for element in elements]

    def get_product_count(self) -> int:
        """
        Get the total number of products displayed
        
        Returns:
            int: Number of products
        """
        elements = self.find_elements(self.INVENTORY_ITEM)
        return len(elements)

    def click_product_by_name(self, product_name: str) -> None:
        """
        Click on a product by its name
        
        Args:
            product_name: Name of the product to click
        """
        product_locator = (By.XPATH, f"//div[text()='{product_name}']")
        self.click(product_locator)

    # Add to Cart Methods
    def add_backpack_to_cart(self) -> None:
        """Add Sauce Labs Backpack to cart"""
        self.click(self.ADD_TO_CART_BACKPACK)

    def add_bike_light_to_cart(self) -> None:
        """Add Sauce Labs Bike Light to cart"""
        self.click(self.ADD_TO_CART_BIKE_LIGHT)

    def add_bolt_tshirt_to_cart(self) -> None:
        """Add Sauce Labs Bolt T-Shirt to cart"""
        self.click(self.ADD_TO_CART_BOLT_TSHIRT)

    def add_fleece_jacket_to_cart(self) -> None:
        """Add Sauce Labs Fleece Jacket to cart"""
        self.click(self.ADD_TO_CART_FLEECE_JACKET)

    def add_onesie_to_cart(self) -> None:
        """Add Sauce Labs Onesie to cart"""
        self.click(self.ADD_TO_CART_ONESIE)

    def add_red_tshirt_to_cart(self) -> None:
        """Add Test.allTheThings() T-Shirt (Red) to cart"""
        self.click(self.ADD_TO_CART_TSHIRT_RED)

    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """
        Add a product to cart by its name (generic method)
        
        Args:
            product_name: Name of the product
        """
        # Convert product name to button ID format
        button_id = "add-to-cart-" + product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        add_button_locator = (By.ID, button_id)
        self.click(add_button_locator)

    # Remove from Cart Methods
    def remove_backpack_from_cart(self) -> None:
        """Remove Sauce Labs Backpack from cart"""
        self.click(self.REMOVE_BACKPACK)

    def remove_bike_light_from_cart(self) -> None:
        """Remove Sauce Labs Bike Light from cart"""
        self.click(self.REMOVE_BIKE_LIGHT)

    def remove_bolt_tshirt_from_cart(self) -> None:
        """Remove Sauce Labs Bolt T-Shirt from cart"""
        self.click(self.REMOVE_BOLT_TSHIRT)

    def remove_fleece_jacket_from_cart(self) -> None:
        """Remove Sauce Labs Fleece Jacket from cart"""
        self.click(self.REMOVE_FLEECE_JACKET)

    def remove_onesie_from_cart(self) -> None:
        """Remove Sauce Labs Onesie from cart"""
        self.click(self.REMOVE_ONESIE)

    def remove_red_tshirt_from_cart(self) -> None:
        """Remove Test.allTheThings() T-Shirt (Red) from cart"""
        self.click(self.REMOVE_TSHIRT_RED)

    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Check if a product's Remove button is displayed (indicating it's in cart)
        
        Args:
            product_name: Name of the product
            
        Returns:
            bool: True if product is in cart
        """
        button_id = "remove-" + product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        remove_button_locator = (By.ID, button_id)
        return self.is_displayed(remove_button_locator)

    # Social Media Methods
    def click_twitter_link(self) -> None:
        """Click Twitter social media link in footer"""
        self.scroll_to_element(self.SOCIAL_TWITTER)
        self.click(self.SOCIAL_TWITTER)

    def click_facebook_link(self) -> None:
        """Click Facebook social media link in footer"""
        self.scroll_to_element(self.SOCIAL_FACEBOOK)
        self.click(self.SOCIAL_FACEBOOK)

    def click_linkedin_link(self) -> None:
        """Click LinkedIn social media link in footer"""
        self.scroll_to_element(self.SOCIAL_LINKEDIN)
        self.click(self.SOCIAL_LINKEDIN)

    def is_footer_displayed(self) -> bool:
        """
        Check if footer is displayed
        
        Returns:
            bool: True if footer is displayed
        """
        return self.is_displayed(self.FOOTER)