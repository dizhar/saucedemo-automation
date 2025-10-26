"""
Common step definitions shared across features
"""

from behave import given, when, then # type: ignore
from src.pages.login_page import LoginPage
from src.pages.products_page import ProductsPage
from src.utils.test_data import test_data
from src.utils.logger import logger


@given('I am logged in as a standard user')
def step_login_as_standard_user(context):
    """Login as standard user (shortcut for common setup)"""
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_login_page()
    context.login_page.wait_for_login_page_to_load()

    credentials = test_data.get_user_credentials("standard")
    context.login_page.login(credentials["username"], credentials["password"])

    context.products_page = ProductsPage(context.driver)
    context.products_page.wait_for_products_page_to_load()

    logger.info("Logged in as standard user")


@given('I am logged in as "{user_type}" user')
def step_login_as_specific_user(context, user_type):
    """Login as a specific user type"""
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_login_page()
    context.login_page.wait_for_login_page_to_load()

    credentials = test_data.get_user_credentials(user_type.lower())
    context.login_page.login(credentials["username"], credentials["password"])

    # Only wait for products page if not locked out user
    if user_type.lower() != "locked_out":
        context.products_page = ProductsPage(context.driver)
        context.products_page.wait_for_products_page_to_load()

    logger.info(f"Logged in as {user_type} user")


@then('the page URL should be "{url}"')
def step_verify_page_url(context, url):
    """Verify current page URL"""
    current_url = context.driver.current_url
    assert current_url == url, f"Expected URL '{url}', got '{current_url}'"
    logger.info(f"Verified: Page URL is '{url}'")


@then('the page URL should contain "{url_part}"')
def step_verify_page_url_contains(context, url_part):
    """Verify page URL contains specific text"""
    current_url = context.driver.current_url
    assert url_part in current_url, f"Expected URL to contain '{url_part}', got '{current_url}'"
    logger.info(f"Verified: Page URL contains '{url_part}'")


@then('the page title should be "{title}"')
def step_verify_page_title(context, title):
    """Verify page title"""
    actual_title = context.driver.title
    assert actual_title == title, f"Expected title '{title}', got '{actual_title}'"
    logger.info(f"Verified: Page title is '{title}'")


@then('I wait for {seconds:d} seconds')
def step_wait_for_seconds(context, seconds):
    """Wait for specified seconds (for debugging/demo purposes)"""
    import time
    time.sleep(seconds)
    logger.info(f"Waited for {seconds} seconds")

@then('I should see an error message containing "{text}"')
def step_verify_error_message_contains_text(context, text):
    """Verify error message contains specific text (works across all pages)"""
    # Try to get error from current page
    error_text = ""
    
    # Check if it's a login page error
    try:
        from src.pages.login_page import LoginPage
        login_page = LoginPage(context.driver)
        if login_page.is_error_message_displayed():
            error_text = login_page.get_error_message()
    except:
        pass
    
    # Check if it's a checkout page error
    if not error_text:
        try:
            from src.pages.checkout_page import CheckoutPage
            checkout_page = CheckoutPage(context.driver)
            if checkout_page.is_error_displayed():
                error_text = checkout_page.get_error_message()
        except:
            pass
    
    assert error_text, "No error message found on the page"
    assert text.lower() in error_text.lower(), \
        f"Expected error to contain '{text}', but got '{error_text}'"
 