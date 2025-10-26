from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page object for SauceDemo checkout pages (info, overview, complete)"""
    
    # Checkout Information Page Locators
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    # Checkout Overview Page Locators
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Checkout Complete Page Locators
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    # Checkout Information Page Methods
    def is_on_checkout_info_page(self):
        """Verify user is on checkout information page"""
        return "checkout-step-one" in self.get_current_url()
    
    def enter_first_name(self, first_name):
        """Enter first name"""
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name):
        """Enter last name"""
        self.send_keys(self.LAST_NAME_INPUT, last_name)
    
    def enter_postal_code(self, postal_code):
        """Enter postal code"""
        self.send_keys(self.POSTAL_CODE_INPUT, postal_code)
    
    def fill_checkout_information(self, first_name, last_name, postal_code):
        """Fill all checkout information fields"""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
    
    def click_continue(self):
        """Click continue button"""
        self.click(self.CONTINUE_BUTTON)
    
    def click_cancel(self):
        """Click cancel button"""
        self.click(self.CANCEL_BUTTON)
    
    def get_error_message(self):
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_displayed(self.ERROR_MESSAGE)
    
    # Checkout Overview Page Methods
    def is_on_checkout_overview_page(self):
        """Verify user is on checkout overview page"""
        return "checkout-step-two" in self.get_current_url()
    
    def get_cart_items_on_overview(self):
        """Get list of cart items on overview page"""
        items = self.find_elements((By.CLASS_NAME, "inventory_item_name"))
        return [item.text for item in items]
    
    def get_subtotal(self):
        """Get subtotal value"""
        text = self.get_text(self.SUBTOTAL_LABEL)
        return float(text.replace("Item total: $", ""))
    
    def get_tax(self):
        """Get tax value"""
        text = self.get_text(self.TAX_LABEL)
        return float(text.replace("Tax: $", ""))
    
    def get_total(self):
        """Get total value"""
        text = self.get_text(self.TOTAL_LABEL)
        return float(text.replace("Total: $", ""))
    
    def click_finish(self):
        """Click finish button"""
        self.click(self.FINISH_BUTTON)
    
    # Checkout Complete Page Methods
    def is_on_checkout_complete_page(self):
        """Verify user is on checkout complete page"""
        return "checkout-complete" in self.get_current_url()
    
    def get_complete_header(self):
        """Get completion header text"""
        return self.get_text(self.COMPLETE_HEADER)
    
    def get_complete_message(self):
        """Get completion message text"""
        return self.get_text(self.COMPLETE_TEXT)
    
    def is_order_complete(self):
        """Check if order completion is displayed"""
        return self.is_displayed(self.COMPLETE_HEADER)
    
    def click_back_home(self):
        """Click back to products button"""
        self.click(self.BACK_HOME_BUTTON)
