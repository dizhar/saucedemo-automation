"""
Step definitions for Login functionality
"""

from behave import given, when, then  # type: ignore
from src.pages.login_page import LoginPage
from src.pages.products_page import ProductsPage
from src.utils.logger import logger
from src.utils.test_data import test_data


@given('I am on the login page')
def step_navigate_to_login_page(context):
    """Navigate to the login page"""
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_login_page()
    context.login_page.wait_for_login_page_to_load()
    logger.info("Navigated to login page")


@when('I login with username "{username}" and password "{password}"')
def step_login_with_credentials(context, username, password):
    """Login with provided credentials"""
    context.login_page = LoginPage(context.driver)
    context.login_page.login(username, password)
    logger.info(f"Attempted login with username: {username}")


@when('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username in the username field"""
    context.login_page = LoginPage(context.driver)
    context.login_page.enter_username(username)
    logger.info(f"Entered username: {username}")


@when('I enter password "{password}"')
def step_enter_password(context, password):
    """Enter password in the password field"""
    context.login_page = LoginPage(context.driver)
    context.login_page.enter_password(password)
    logger.info(f"Entered password: {password}")


@when('I click the login button')
def step_click_login_button(context):
    """Click the login button"""
    context.login_page = LoginPage(context.driver)
    context.login_page.click_login_button()
    logger.info("Clicked login button")


@then('I should be on the products page')
def step_verify_on_products_page(context):
    """Verify user is redirected to products page"""
    context.products_page = ProductsPage(context.driver)
    context.products_page.wait_for_products_page_to_load()
    assert context.products_page.is_on_products_page(), "Not on products page"
    logger.info("Verified: User is on products page")


@then('I should see the app logo')
def step_verify_app_logo(context):
    """Verify app logo is displayed"""
    context.products_page = ProductsPage(context.driver)
    assert context.products_page.is_on_products_page(), "App logo not displayed"
    logo_text = context.products_page.get_page_title()
    assert logo_text == "Swag Labs", f"Expected 'Swag Labs', got '{logo_text}'"
    logger.info(f"Verified: App logo displays '{logo_text}'")


@then('I should see an error message')
def step_verify_error_message_displayed(context):
    """Verify error message is displayed"""
    context.login_page = LoginPage(context.driver)
    assert context.login_page.is_error_message_displayed(), "Error message not displayed"
    error_text = context.login_page.get_error_message()
    logger.info(f"Verified: Error message displayed - '{error_text}'")


@then('I should remain on the login page')
def step_verify_remain_on_login_page(context):
    """Verify user remains on the login page"""
    context.login_page = LoginPage(context.driver)
    assert context.login_page.is_on_login_page(), "Not on login page"
    logger.info("Verified: User remained on login page")


# ==================== EMPTY STRING HANDLERS ====================
# Explicit steps for empty string parameters (Behave quirk workaround)

@when('I enter username ""')
def step_enter_empty_username(context):
    """Enter empty username"""
    step_enter_username(context, "")


@when('I enter password ""')
def step_enter_empty_password(context):
    """Enter empty password"""
    step_enter_password(context, "")


# ==================== DATA-DRIVEN STEPS USING users.json ====================

@when('I login with valid user "{user_type}"')
def step_login_with_valid_user(context, user_type):
    """Login with a valid user from users.json based on type (e.g., 'standard', 'problem', 'performance_glitch')"""
    valid_users = test_data.get_valid_users()

    # Find user by matching the user_type with username prefix
    user = None
    for u in valid_users:
        if user_type in u.get('username', ''):
            user = u
            break

    if not user:
        # Fallback to first user if type not found
        user = valid_users[0] if valid_users else {'username': '', 'password': ''}

    context.login_page = LoginPage(context.driver)
    context.login_page.login(user['username'], user['password'])
    logger.info(f"Attempted login with {user.get('description', user['username'])}")


@when('I login with locked user')
def step_login_with_locked_user(context):
    """Login with a locked user from users.json"""
    locked_users = test_data.get_locked_users()

    if locked_users:
        user = locked_users[0]
        context.login_page = LoginPage(context.driver)
        context.login_page.login(user['username'], user['password'])
        logger.info(f"Attempted login with locked user: {user['username']}")


@when('I login with invalid credentials case "{case_type}"')
def step_login_with_invalid_credentials(context, case_type):
    """
    Login with invalid credentials from users.json
    case_type: 'invalid_username', 'invalid_password', or 'both_invalid'
    """
    invalid_creds = test_data.get_invalid_credentials()

    # Map case_type to description keywords
    case_map = {
        'invalid_username': 'Invalid username',
        'invalid_password': 'invalid password',
        'both_invalid': 'Invalid username and password'
    }

    user = None
    search_term = case_map.get(case_type, '')

    for cred in invalid_creds:
        if search_term.lower() in cred.get('description', '').lower():
            user = cred
            break

    if not user:
        user = invalid_creds[0] if invalid_creds else {'username': '', 'password': ''}

    context.login_page = LoginPage(context.driver)
    context.login_page.login(user['username'], user['password'])
    logger.info(f"Attempted login with {user.get('description', 'invalid credentials')}")


@when('I login with empty credentials case "{case_type}"')
def step_login_with_empty_credentials(context, case_type):
    """
    Login with empty credentials from users.json
    case_type: 'empty_username', 'empty_password', or 'both_empty'
    """
    empty_creds = test_data.get_empty_credentials()

    # Map case_type to description keywords
    case_map = {
        'empty_username': 'Empty username',
        'empty_password': 'empty password',
        'both_empty': 'Empty username and password'
    }

    user = None
    search_term = case_map.get(case_type, '')

    for cred in empty_creds:
        if search_term.lower() in cred.get('description', '').lower():
            user = cred
            break

    if not user:
        user = empty_creds[0] if empty_creds else {'username': '', 'password': ''}

    context.login_page = LoginPage(context.driver)
    context.login_page.enter_username(user['username'])
    context.login_page.enter_password(user['password'])
    context.login_page.click_login_button()
    logger.info(f"Attempted login with {user.get('description', 'empty credentials')}")


@then('I should see the expected error for "{error_type}"')
def step_verify_expected_error(context, error_type):
    """Verify the expected error message based on error type"""
    context.login_page = LoginPage(context.driver)
    assert context.login_page.is_error_message_displayed(), "Error message not displayed"

    actual_error = context.login_page.get_error_message()

    # Get expected error from users.json based on error_type
    expected_error = ""

    if error_type == "locked":
        locked_users = test_data.get_locked_users()
        if locked_users:
            expected_error = locked_users[0].get('expected_error', '')
    elif error_type in ['invalid_username', 'invalid_password', 'both_invalid']:
        invalid_creds = test_data.get_invalid_credentials()
        if invalid_creds:
            expected_error = invalid_creds[0].get('expected_error', '')
    elif error_type in ['empty_username', 'empty_password']:
        empty_creds = test_data.get_empty_credentials()
        for cred in empty_creds:
            if error_type.replace('_', ' ').lower() in cred.get('description', '').lower():
                expected_error = cred.get('expected_error', '')
                break

    if expected_error:
        assert expected_error in actual_error, f"Expected error '{expected_error}' not found in '{actual_error}'"
        logger.info(f"Verified: Expected error message - '{expected_error}'")
    else:
        logger.info(f"Verified: Error message displayed - '{actual_error}'")