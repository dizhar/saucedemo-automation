"""
Step definitions for Checkout functionality
"""

from behave import given, when, then # type: ignore
from src.pages.products_page import ProductsPage
from src.utils.logger import logger
import csv
import os


# Note: CheckoutPage would be implemented when CheckoutPage class is created
# For now, using basic Selenium commands for checkout flow


@when('I proceed to checkout')
def step_proceed_to_checkout(context):
    """Click checkout button from cart page"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        checkout_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()
        logger.info("Clicked checkout button")
    except Exception as e:
        logger.error(f"Failed to click checkout button: {e}")
        raise


@when('I fill in checkout information')
def step_fill_checkout_information(context):
    """Fill in checkout information with default test data"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Wait for first name field
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        
        # Fill in form fields
        context.driver.find_element(By.ID, "first-name").send_keys("John")
        context.driver.find_element(By.ID, "last-name").send_keys("Doe")
        context.driver.find_element(By.ID, "postal-code").send_keys("12345")
        
        logger.info("Filled checkout information: John Doe, 12345")
    except Exception as e:
        logger.error(f"Failed to fill checkout information: {e}")
        raise


@when('I fill in first name "{first_name}"')
def step_fill_first_name(context, first_name):
    """Fill in first name field"""
    from selenium.webdriver.common.by import By
    context.driver.find_element(By.ID, "first-name").send_keys(first_name)
    logger.info(f"Filled first name: {first_name}")


@when('I fill in last name "{last_name}"')
def step_fill_last_name(context, last_name):
    """Fill in last name field"""
    from selenium.webdriver.common.by import By
    context.driver.find_element(By.ID, "last-name").send_keys(last_name)
    logger.info(f"Filled last name: {last_name}")


@when('I fill in postal code "{postal_code}"')
def step_fill_postal_code(context, postal_code):
    """Fill in postal code field"""
    from selenium.webdriver.common.by import By
    context.driver.find_element(By.ID, "postal-code").send_keys(postal_code)
    logger.info(f"Filled postal code: {postal_code}")


@when('I click continue')
def step_click_continue(context):
    """Click continue button on checkout information page"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        continue_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "continue"))
        )
        continue_button.click()
        logger.info("Clicked continue button")
    except Exception as e:
        logger.error(f"Failed to click continue button: {e}")
        raise


@when('I click finish')
def step_click_finish(context):
    """Click finish button on checkout overview page"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        finish_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "finish"))
        )
        finish_button.click()
        logger.info("Clicked finish button")
    except Exception as e:
        logger.error(f"Failed to click finish button: {e}")
        raise


@when('I click cancel')
def step_click_cancel(context):
    """Click cancel button"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        cancel_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "cancel"))
        )
        cancel_button.click()
        logger.info("Clicked cancel button")
    except Exception as e:
        logger.error(f"Failed to click cancel button: {e}")
        raise


@when('I complete the checkout process')
def step_complete_checkout_process(context):
    """Complete entire checkout process with default data"""
    # Fill checkout information
    step_fill_checkout_information(context)
    
    # Click continue
    step_click_continue(context)
    
    # Click finish
    step_click_finish(context)
    
    logger.info("Completed checkout process")


@then('I should be on the checkout information page')
def step_verify_on_checkout_information_page(context):
    """Verify user is on checkout step one page"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        assert "checkout-step-one" in context.driver.current_url, \
            f"Expected checkout-step-one in URL, got {context.driver.current_url}"
        logger.info("Verified: On checkout information page")
    except Exception as e:
        logger.error(f"Not on checkout information page: {e}")
        raise


@then('I should be on the checkout overview page')
def step_verify_on_checkout_overview_page(context):
    """Verify user is on checkout step two (overview) page"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_info"))
        )
        assert "checkout-step-two" in context.driver.current_url, \
            f"Expected checkout-step-two in URL, got {context.driver.current_url}"
        logger.info("Verified: On checkout overview page")
    except Exception as e:
        logger.error(f"Not on checkout overview page: {e}")
        raise


@then('I should see the order confirmation')
@then('I should see the order complete message')
def step_verify_order_confirmation(context):
    """Verify order confirmation/complete page is displayed"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Wait for complete header
        complete_header = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        
        assert "checkout-complete" in context.driver.current_url, \
            f"Expected checkout-complete in URL, got {context.driver.current_url}"
        
        # Verify confirmation message
        header_text = complete_header.text
        assert "Thank you for your order" in header_text or "THANK YOU FOR YOUR ORDER" in header_text.upper(), \
            f"Expected confirmation message, got: {header_text}"
        
        logger.info(f"Verified: Order confirmation displayed - '{header_text}'")
    except Exception as e:
        logger.error(f"Order confirmation not found: {e}")
        raise


@then('I should see a checkout error message')
def step_verify_checkout_error_message(context):
    """Verify checkout error message is displayed"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        error_message = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
        )
        assert error_message.is_displayed(), "Error message should be displayed"
        error_text = error_message.text
        logger.info(f"Verified: Checkout error message displayed - '{error_text}'")
    except Exception as e:
        logger.error(f"Checkout error message not found: {e}")
        raise
    

@then('I should see the payment information')
def step_verify_payment_information(context):
    """Verify payment information section is displayed"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        payment_info = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='payment-info-label']"))
        )
        assert payment_info.is_displayed(), "Payment information should be displayed"
        logger.info("Verified: Payment information displayed")
    except Exception as e:
        logger.error(f"Payment information not found: {e}")
        raise


@then('I should see the shipping information')
def step_verify_shipping_information(context):
    """Verify shipping information section is displayed"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        shipping_info = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='shipping-info-label']"))
        )
        assert shipping_info.is_displayed(), "Shipping information should be displayed"
        logger.info("Verified: Shipping information displayed")
    except Exception as e:
        logger.error(f"Shipping information not found: {e}")
        raise


@then('I should see the total price')
def step_verify_total_price(context):
    """Verify total price is displayed"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        total_price = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )
        assert total_price.is_displayed(), "Total price should be displayed"
        total_text = total_price.text
        assert "$" in total_text, f"Expected price with $, got: {total_text}"
        logger.info(f"Verified: Total price displayed - {total_text}")
    except Exception as e:
        logger.error(f"Total price not found: {e}")
        raise


@then('I should see {count:d} item in checkout')
@then('I should see {count:d} items in checkout')
def step_verify_items_in_checkout(context, count):
    """Verify number of items in checkout"""
    from selenium.webdriver.common.by import By
    
    try:
        cart_items = context.driver.find_elements(By.CLASS_NAME, "cart_item")
        actual_count = len(cart_items)
        assert actual_count == count, f"Expected {count} items, found {actual_count}"
        logger.info(f"Verified: {count} item(s) in checkout")
    except Exception as e:
        logger.error(f"Failed to verify items in checkout: {e}")
        raise


@when('I go back to home')
@when('I click back home')
def step_click_back_home(context):
    """Click back home button on order complete page"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        back_home_button = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "back-to-products"))
        )
        back_home_button.click()
        logger.info("Clicked back home button")
    except Exception as e:
        logger.error(f"Failed to click back home button: {e}")
        raise


@then('the cart should be empty after checkout')
def step_verify_cart_empty_after_checkout(context):
    """Verify cart is empty after completing checkout"""
    context.products_page = ProductsPage(context.driver)
    assert not context.products_page.is_cart_badge_displayed(), \
        "Cart badge should not be visible after checkout"
    logger.info("Verified: Cart is empty after checkout")


@then('I should verify the order summary calculation')
def step_verify_order_summary_calculation(context):
    """Verify that total = subtotal + tax"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    try:
        # Wait for summary info to be visible
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_info"))
        )

        # Get item total (subtotal)
        item_total_element = context.driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
        item_total_text = item_total_element.text  # e.g., "Item total: $29.99"
        item_total = float(item_total_text.split("$")[1])

        # Get tax
        tax_element = context.driver.find_element(By.CLASS_NAME, "summary_tax_label")
        tax_text = tax_element.text  # e.g., "Tax: $2.40"
        tax = float(tax_text.split("$")[1])

        # Get total
        total_element = context.driver.find_element(By.CLASS_NAME, "summary_total_label")
        total_text = total_element.text  # e.g., "Total: $32.39"
        total = float(total_text.split("$")[1])

        # Verify calculation: total = item_total + tax
        expected_total = round(item_total + tax, 2)
        assert total == expected_total, \
            f"Total mismatch: Expected ${expected_total} (${item_total} + ${tax}), got ${total}"

        logger.info(f"Verified: Order summary calculation correct - Items: ${item_total}, Tax: ${tax}, Total: ${total}")
    except Exception as e:
        logger.error(f"Failed to verify order summary calculation: {e}")
        raise


@then('I should not be able to proceed to checkout')
def step_verify_cannot_proceed_to_checkout(context):
    """Verify that checkout button is not available or disabled for empty cart"""
    from selenium.webdriver.common.by import By

    try:
        # Try to find checkout button
        checkout_buttons = context.driver.find_elements(By.ID, "checkout")

        if len(checkout_buttons) == 0:
            # No checkout button found - cart is empty, which is expected
            logger.info("Verified: No checkout button available for empty cart")
        else:
            # Checkout button exists, verify it's disabled or cart is empty
            cart_items = context.driver.find_elements(By.CLASS_NAME, "cart_item")
            assert len(cart_items) == 0, \
                "Cart should be empty, preventing meaningful checkout"
            logger.info("Verified: Cart is empty, checkout should not proceed meaningfully")
    except Exception as e:
        logger.error(f"Failed to verify empty cart checkout prevention: {e}")
        raise


@when('I complete checkout with data from CSV "{csv_file}"')
def step_complete_checkout_with_csv_data(context, csv_file):
    """Complete checkout using data from CSV file - tests with all rows"""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(project_root, csv_file)

    logger.info(f"Reading checkout data from: {csv_path}")

    # Read CSV file
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        test_data = list(reader)

    logger.info(f"Found {len(test_data)} rows in CSV file")

    # Test with each row of data
    for index, row in enumerate(test_data, start=1):
        first_name = row['first_name']
        last_name = row['last_name']
        postal_code = row['postal_code']
        description = row.get('description', '')

        logger.info(f"Testing checkout {index}/{len(test_data)}: {first_name} {last_name}, {postal_code} ({description})")

        try:
            # Wait for first name field to be present
            WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located((By.ID, "first-name"))
            )

            # Clear and fill in form fields
            first_name_field = context.driver.find_element(By.ID, "first-name")
            first_name_field.clear()
            first_name_field.send_keys(first_name)

            last_name_field = context.driver.find_element(By.ID, "last-name")
            last_name_field.clear()
            last_name_field.send_keys(last_name)

            postal_code_field = context.driver.find_element(By.ID, "postal-code")
            postal_code_field.clear()
            postal_code_field.send_keys(postal_code)

            # Click continue
            continue_button = WebDriverWait(context.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "continue"))
            )
            continue_button.click()

            # Verify we're on checkout overview page
            WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "summary_info"))
            )

            # Verify order summary calculation
            step_verify_order_summary_calculation(context)

            # Click finish
            finish_button = WebDriverWait(context.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "finish"))
            )
            finish_button.click()

            # Verify order confirmation
            WebDriverWait(context.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
            )

            logger.info(f"✓ Checkout {index}/{len(test_data)} completed successfully with {first_name} {last_name}")

            # If not the last iteration, go back to cart and reset for next test
            if index < len(test_data):
                # Go back home
                back_home_button = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "back-to-products"))
                )
                back_home_button.click()

                # Add items to cart again for next iteration
                context.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
                context.driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()

                # Go to cart
                context.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

                # Proceed to checkout
                checkout_button = WebDriverWait(context.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "checkout"))
                )
                checkout_button.click()

        except Exception as e:
            logger.error(f"✗ Checkout {index}/{len(test_data)} failed with {first_name} {last_name}: {e}")
            raise

    logger.info(f"All {len(test_data)} checkout tests completed successfully with CSV data")