"""
Step definitions for Products/Inventory functionality
"""

from behave import given, when, then # type: ignore
from src.pages.products_page import ProductsPage
from src.utils.logger import logger

@given('I add "{product_name}" to cart')
@when('I add "{product_name}" to cart')
def step_add_product_to_cart(context, product_name):
    """Add a specific product to cart by name"""
    context.products_page = ProductsPage(context.driver)
    
    if product_name.lower() == "sauce labs backpack":
        context.products_page.add_backpack_to_cart()
    elif product_name.lower() == "sauce labs bike light":
        context.products_page.add_bike_light_to_cart()
    elif product_name.lower() == "sauce labs bolt t-shirt":
        context.products_page.add_bolt_tshirt_to_cart()
    elif product_name.lower() == "sauce labs fleece jacket":
        context.products_page.add_fleece_jacket_to_cart()
    elif product_name.lower() == "sauce labs onesie":
        context.products_page.add_onesie_to_cart()
    else:
        context.products_page.add_product_to_cart_by_name(product_name)
    
    logger.info(f"Added '{product_name}' to cart")


@when('I remove "{product_name}" from cart')
def step_remove_product_from_cart(context, product_name):
    """Remove a specific product from cart"""
    context.products_page = ProductsPage(context.driver)
    
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


@when('I sort products by "{sort_option}"')
def step_sort_products(context, sort_option):
    """Sort products by given option"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.select_sort_option(sort_option)
    logger.info(f"Sorted products by: {sort_option}")


@when('I click on product "{product_name}"')
def step_click_product(context, product_name):
    """Click on a specific product"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.click_product_by_name(product_name)
    logger.info(f"Clicked on product: {product_name}")


@when('I click the shopping cart')
def step_click_shopping_cart(context):
    """Click the shopping cart icon"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.click_shopping_cart()
    logger.info("Clicked shopping cart")


@when('I open the menu')
def step_open_menu(context):
    """Open the hamburger menu"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.open_menu()
    logger.info("Opened menu")


@when('I click logout')
def step_click_logout(context):
    """Click logout from menu"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.click_logout()
    logger.info("Clicked logout")


@then('I should see {count:d} products')
def step_verify_product_count(context, count):
    """Verify the number of products displayed"""
    context.products_page = ProductsPage(context.driver)
    actual_count = context.products_page.get_product_count()
    assert actual_count == count, f"Expected {count} products, found {actual_count}"
    logger.info(f"Verified: {count} products displayed")


@then('the cart badge should show {count:d}')
def step_verify_cart_badge_count(context, count):
    """Verify the cart badge shows correct count"""
    context.products_page = ProductsPage(context.driver)
    
    if count == 0:
        assert not context.products_page.is_cart_badge_displayed(), "Cart badge should not be displayed"
        logger.info("Verified: Cart badge not displayed (0 items)")
    else:
        badge_count = context.products_page.get_cart_badge_count()
        assert badge_count == str(count), f"Expected cart badge '{count}', got '{badge_count}'"
        logger.info(f"Verified: Cart badge shows {count}")


@then('"{product_name}" should be in the cart')
def step_verify_product_in_cart(context, product_name):
    """Verify product is in cart (Remove button visible)"""
    context.products_page = ProductsPage(context.driver)
    assert context.products_page.is_product_in_cart(product_name), f"'{product_name}' not in cart"
    logger.info(f"Verified: '{product_name}' is in cart")


@then('the products should be sorted by name A to Z')
def step_verify_products_sorted_az(context):
    """Verify products are sorted alphabetically A-Z"""
    context.products_page = ProductsPage(context.driver)
    product_names = context.products_page.get_all_product_names()
    sorted_names = sorted(product_names)
    assert product_names == sorted_names, f"Products not sorted A-Z: {product_names}"
    logger.info("Verified: Products sorted A to Z")


@then('the products should be sorted by name Z to A')
def step_verify_products_sorted_za(context):
    """Verify products are sorted alphabetically Z-A"""
    context.products_page = ProductsPage(context.driver)
    product_names = context.products_page.get_all_product_names()
    sorted_names = sorted(product_names, reverse=True)
    assert product_names == sorted_names, f"Products not sorted Z-A: {product_names}"
    logger.info("Verified: Products sorted Z to A")


@then('the products should be sorted by price low to high')
def step_verify_products_sorted_price_low_high(context):
    """Verify products are sorted by price low to high"""
    context.products_page = ProductsPage(context.driver)
    prices = context.products_page.get_all_product_prices()
    # Convert prices from "$29.99" to float 29.99
    price_values = [float(price.replace('$', '')) for price in prices]
    sorted_prices = sorted(price_values)
    assert price_values == sorted_prices, f"Products not sorted by price (low to high): {prices}"
    logger.info("Verified: Products sorted by price (low to high)")


@then('the products should be sorted by price high to low')
def step_verify_products_sorted_price_high_low(context):
    """Verify products are sorted by price high to low"""
    context.products_page = ProductsPage(context.driver)
    prices = context.products_page.get_all_product_prices()
    # Convert prices from "$29.99" to float 29.99
    price_values = [float(price.replace('$', '')) for price in prices]
    sorted_prices = sorted(price_values, reverse=True)
    assert price_values == sorted_prices, f"Products not sorted by price (high to low): {prices}"
    logger.info("Verified: Products sorted by price (high to low)")


@then('all product names should not be empty')
def step_verify_all_product_names_not_empty(context):
    """Verify all product names are not empty"""
    context.products_page = ProductsPage(context.driver)
    product_names = context.products_page.get_all_product_names()

    # Assert that there are products
    assert len(product_names) > 0, "No products found on the page"

    # Assert that all product names are not empty
    for i, name in enumerate(product_names, 1):
        assert name and name.strip(), f"Product {i} has an empty name"

    logger.info(f"Verified: All {len(product_names)} product names are not empty")


@then('all product prices should be greater than {min_price:d}')
def step_verify_all_product_prices_greater_than(context, min_price):
    """Verify all product prices are greater than a minimum value"""
    context.products_page = ProductsPage(context.driver)
    prices = context.products_page.get_all_product_prices()

    # Assert that there are prices
    assert len(prices) > 0, "No product prices found on the page"

    # Convert prices from "$29.99" to float 29.99 and verify each is greater than min_price
    for i, price_str in enumerate(prices, 1):
        # Remove '$' and convert to float
        price_value = float(price_str.replace('$', ''))
        assert price_value > min_price, f"Product {i} price ${price_value} is not greater than ${min_price}"

    logger.info(f"Verified: All {len(prices)} product prices are greater than ${min_price}")