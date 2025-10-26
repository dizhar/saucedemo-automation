"""
Step definitions for Shopping Cart functionality
"""

from behave import given, when, then # type: ignore
from src.pages.products_page import ProductsPage
from src.utils.logger import logger


# Note: Cart page would be implemented when CartPage class is created
# For now, using ProductsPage for cart badge verification


@when('I view the shopping cart')
def step_view_shopping_cart(context):
    """Click on shopping cart icon to view cart"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.click_shopping_cart()
    logger.info("Navigated to shopping cart")


@then('the cart should be empty')
def step_verify_cart_empty(context):
    """Verify cart has no items"""
    context.products_page = ProductsPage(context.driver)
    assert not context.products_page.is_cart_badge_displayed(), "Cart badge should not be visible when empty"
    logger.info("Verified: Cart is empty")


@then('the cart should contain {count:d} item')
@then('the cart should contain {count:d} items')
def step_verify_cart_item_count(context, count):
    """Verify cart contains specific number of items"""
    context.products_page = ProductsPage(context.driver)
    
    if count == 0:
        assert not context.products_page.is_cart_badge_displayed(), "Cart badge should not be visible when empty"
        logger.info("Verified: Cart has 0 items")
    else:
        assert context.products_page.is_cart_badge_displayed(), "Cart badge should be visible"
        badge_count = int(context.products_page.get_cart_badge_count())
        assert badge_count == count, f"Expected {count} items in cart, found {badge_count}"
        logger.info(f"Verified: Cart has {count} item(s)")


@then('the cart badge should display {count:d}')
def step_verify_cart_badge_displays_count(context, count):
    """Verify cart badge displays specific number"""
    context.products_page = ProductsPage(context.driver)
    badge_count = int(context.products_page.get_cart_badge_count())
    assert badge_count == count, f"Expected cart badge to show {count}, got {badge_count}"
    logger.info(f"Verified: Cart badge displays {count}")


@then('the cart badge should not be visible')
def step_verify_cart_badge_not_visible(context):
    """Verify cart badge is not displayed"""
    context.products_page = ProductsPage(context.driver)
    assert not context.products_page.is_cart_badge_displayed(), "Cart badge should not be visible"
    logger.info("Verified: Cart badge not visible")


@then('the cart badge should be visible')
def step_verify_cart_badge_visible(context):
    """Verify cart badge is displayed"""
    context.products_page = ProductsPage(context.driver)
    assert context.products_page.is_cart_badge_displayed(), "Cart badge should be visible"
    logger.info("Verified: Cart badge is visible")

@given('I add multiple products to cart') 
@when('I add multiple products to cart')
def step_add_multiple_products(context):
    """Add multiple products to cart"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.add_backpack_to_cart()
    context.products_page.add_bike_light_to_cart()
    context.products_page.add_bolt_tshirt_to_cart()
    logger.info("Added 3 products to cart")


@when('I remove all items from cart')
def step_remove_all_items(context):
    """Remove all items from cart"""
    context.products_page = ProductsPage(context.driver)
    
    # Try to remove each product (ignore if not in cart)
    try:
        context.products_page.remove_backpack_from_cart()
    except:
        pass
    
    try:
        context.products_page.remove_bike_light_from_cart()
    except:
        pass
    
    try:
        context.products_page.remove_bolt_tshirt_from_cart()
    except:
        pass
    
    try:
        context.products_page.remove_fleece_jacket_from_cart()
    except:
        pass
    
    try:
        context.products_page.remove_onesie_from_cart()
    except:
        pass
    
    try:
        context.products_page.remove_red_tshirt_from_cart()
    except:
        pass
    
    logger.info("Removed all items from cart")

@given('I add all products to cart')
@when('I add all products to cart')
def step_add_all_products(context):
    """Add all available products to cart"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.add_backpack_to_cart()
    context.products_page.add_bike_light_to_cart()
    context.products_page.add_bolt_tshirt_to_cart()
    context.products_page.add_fleece_jacket_to_cart()
    context.products_page.add_onesie_to_cart()
    context.products_page.add_red_tshirt_to_cart()
    logger.info("Added all 6 products to cart")


@then('all products should be in the cart')
def step_verify_all_products_in_cart(context):
    """Verify all products are in cart"""
    context.products_page = ProductsPage(context.driver)
    
    # Check cart badge shows 6
    badge_count = int(context.products_page.get_cart_badge_count())
    assert badge_count == 6, f"Expected 6 items in cart, found {badge_count}"
    
    # Verify each product shows Remove button
    assert context.products_page.is_product_in_cart("sauce-labs-backpack"), "Backpack not in cart"
    assert context.products_page.is_product_in_cart("sauce-labs-bike-light"), "Bike Light not in cart"
    assert context.products_page.is_product_in_cart("sauce-labs-bolt-t-shirt"), "Bolt T-Shirt not in cart"
    assert context.products_page.is_product_in_cart("sauce-labs-fleece-jacket"), "Fleece Jacket not in cart"
    assert context.products_page.is_product_in_cart("sauce-labs-onesie"), "Onesie not in cart"
    assert context.products_page.is_product_in_cart("test.allthethings()-t-shirt-(red)"), "Red T-Shirt not in cart"
    
    logger.info("Verified: All 6 products are in cart")

@given('I add {count:d} random products to cart')
@when('I add {count:d} random products to cart')
def step_add_random_products(context, count):
    """Add specified number of random products to cart"""
    context.products_page = ProductsPage(context.driver)
    
    products = [
        context.products_page.add_backpack_to_cart,
        context.products_page.add_bike_light_to_cart,
        context.products_page.add_bolt_tshirt_to_cart,
        context.products_page.add_fleece_jacket_to_cart,
        context.products_page.add_onesie_to_cart,
        context.products_page.add_red_tshirt_to_cart
    ]
    
    for i in range(min(count, len(products))):
        products[i]()
    
    logger.info(f"Added {count} products to cart")


@then('I should be able to remove "{product_name}" from cart')
def step_verify_can_remove_product(context, product_name):
    """Verify product can be removed from cart"""
    context.products_page = ProductsPage(context.driver)
    
    # Verify product is in cart first
    assert context.products_page.is_product_in_cart(product_name), f"'{product_name}' not in cart"
    
    # Remove the product
    if product_name.lower() == "sauce labs backpack":
        context.products_page.remove_backpack_from_cart()
    elif product_name.lower() == "sauce labs bike light":
        context.products_page.remove_bike_light_from_cart()
    elif product_name.lower() == "sauce labs bolt t-shirt":
        context.products_page.remove_bolt_tshirt_from_cart()
    elif product_name.lower() == "sauce labs fleece jacket":
        context.products_page.remove_fleece_jacket_from_cart()
    elif product_name.lower() == "sauce labs onesie":
        context.products_page.remove_onesie_from_cart()
    
    logger.info(f"Removed '{product_name}' from cart")


@then('"{product_name}" should not be in the cart')
def step_verify_product_not_in_cart(context, product_name):
    """Verify product is not in cart"""
    context.products_page = ProductsPage(context.driver)
    assert not context.products_page.is_product_in_cart(product_name), f"'{product_name}' should not be in cart"
    logger.info(f"Verified: '{product_name}' is not in cart")


@when('I continue shopping')
def step_continue_shopping(context):
    """Continue shopping (go back to products page)"""
    # This would typically click a "Continue Shopping" button on cart page
    # For now, just log the action
    logger.info("Continued shopping")


@then('the cart icon should be clickable')
def step_verify_cart_icon_clickable(context):
    """Verify cart icon is clickable"""
    context.products_page = ProductsPage(context.driver)
    # Just verify the element is displayed (implies it's clickable)
    from selenium.webdriver.common.by import By
    cart_icon = context.driver.find_element(*context.products_page.SHOPPING_CART_LINK)
    assert cart_icon.is_displayed(), "Cart icon should be displayed"
    assert cart_icon.is_enabled(), "Cart icon should be enabled"
    logger.info("Verified: Cart icon is clickable")