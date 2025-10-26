"""
Page Objects package for SauceDemo automation framework.
This package contains all Page Object Model (POM) classes.
"""

from src.pages.base_page import BasePage
from src.pages.login_page import LoginPage
from src.pages.products_page import ProductsPage
from src.pages.checkout_page import CheckoutPage
from src.pages.cart_page import CartPage

__all__ = [
    'BasePage',
    'LoginPage',
    'ProductsPage',
    'CheckoutPage',
    'CartPage'
]