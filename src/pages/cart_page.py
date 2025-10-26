from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class CartPage(BasePage):
    """Page object for SauceDemo shopping cart page"""
    
    # Locators
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    
    # Dynamic locators
    REMOVE_BUTTON_TEMPLATE = "//div[text()='{}']/ancestor::div[@class='cart_item']//button"
    ITEM_NAME_TEMPLATE = "//div[text()='{}']"
    ITEM_PRICE_TEMPLATE = "//div[text()='{}']/ancestor::div[@class='cart_item']//div[@class='inventory_item_price']"
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_on_cart_page(self):
        """Verify user is on cart page"""
        return "cart.html" in self.get_current_url()
    
    def get_cart_item_count(self):
        """Get count of items in cart"""
        try:
            items = self.find_elements(self.CART_ITEMS)
            return len(items)
        except:
            return 0
    
    def get_cart_item_names(self):
        """Get list of all item names in cart"""
        items = self.find_elements((By.CLASS_NAME, "inventory_item_name"))
        return [item.text for item in items]
    
    def is_item_in_cart(self, item_name):
        """Check if specific item is in cart"""
        locator = (By.XPATH, self.ITEM_NAME_TEMPLATE.format(item_name))
        return self.is_displayed(locator)
    
    def remove_item_from_cart(self, item_name):
        """Remove item from cart by name"""
        locator = (By.XPATH, self.REMOVE_BUTTON_TEMPLATE.format(item_name))
        self.click(locator)
    
    def get_item_price(self, item_name):
        """Get price of specific item in cart"""
        locator = (By.XPATH, self.ITEM_PRICE_TEMPLATE.format(item_name))
        return self.get_text(locator)
    
    def click_continue_shopping(self):
        """Click continue shopping button"""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
    
    def click_checkout(self):
        """Click checkout button"""
        self.click(self.CHECKOUT_BUTTON)
    
    def get_total_cart_value(self):
        """Calculate total value of all items in cart"""
        prices = self.find_elements((By.CLASS_NAME, "inventory_item_price"))
        total = sum([float(price.text.replace("$", "")) for price in prices])
        return total
