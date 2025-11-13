"""
Behave environment setup and teardown hooks.
"""

from datetime import datetime
import os
import warnings
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from src.utils.config import config
from src.utils.logger import logger
from urllib3.exceptions import NotOpenSSLWarning

# Suppress OpenSSL warning
warnings.filterwarnings('ignore', category=NotOpenSSLWarning)


# =============================================================================
# HOOKS
# =============================================================================

def before_all(context):
    """
    Runs once before all tests.
    """
    logger.info("=" * 80)
    logger.info("Starting Test Execution")
    logger.info("=" * 80)
    config.create_directories()


def before_scenario(context, scenario):
    """
    Runs before each scenario.
    """
    logger.info(f"🎬 Starting Scenario: {scenario.name}")
    context.driver = get_driver(config.BROWSER)

    # Set timeouts
    context.driver.implicitly_wait(config.IMPLICIT_WAIT)
    context.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
    context.driver.set_script_timeout(config.SCRIPT_TIMEOUT)

    # Set window size or maximize
    if config.MAXIMIZE_WINDOW:
        context.driver.maximize_window()
    else:
        context.driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

    logger.info(f"Browser initialized: {config.BROWSER}")


def after_scenario(context, scenario):
    """
    Cleanup after each scenario.
    """
    try:
        if hasattr(context, 'driver') and scenario.status.name == "failed":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in scenario.name)
            screenshot_name = f"failed_{safe_name}_{timestamp}.png"

            screenshots_dir = getattr(config, "SCREENSHOTS_DIR", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            screenshot_path = os.path.join(screenshots_dir, screenshot_name)
            context.driver.save_screenshot(screenshot_path)
            logger.info(f"📸 Screenshot saved: {screenshot_path}")

    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")

    finally:
        try:
            if hasattr(context, 'driver'):
                # Quit driver
                context.driver.quit()

                # Clean up temp Chrome profile
                temp_dir = getattr(context.driver, "_temp_profile_dir", None)
                if temp_dir and os.path.isdir(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    logger.debug(f"Removed temp Chrome profile: {temp_dir}")

                logger.info("Browser closed.")
        except Exception as e:
            logger.warning(f"Error during driver quit/cleanup: {e}")


def after_all(_context):
    """
    Runs once after all tests.
    """
    logger.info("=" * 80)
    logger.info("Test Execution Completed")
    logger.info("=" * 80)


# =============================================================================
# DRIVER SETUP
# =============================================================================

def fix_chromedriver_permissions(driver_path: str) -> str:
    """
    Ensure ChromeDriver is executable.
    """
    try:
        if os.path.exists(driver_path):
            os.chmod(driver_path, 0o755)
            logger.info(f"Fixed permissions for: {driver_path}")
        else:
            logger.warning(f"ChromeDriver not found at: {driver_path}")
    except Exception as e:
        logger.warning(f"Could not fix permissions: {e}")
    return driver_path


def get_driver(browser_name: str):
    """
    Initialize and return WebDriver based on browser name.
    Supports both local and remote Selenium Grid.
    """
    browser_name = browser_name.lower()
    
    # Check if using remote Selenium Grid (Docker mode)
    remote_url = config.SELENIUM_REMOTE_URL
    
    if remote_url:
        logger.info(f"🌐 Connecting to remote Selenium Grid: {remote_url}")
        
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            # Disable password manager and popups for remote
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            }
            options.add_experimental_option("prefs", prefs)
            
            driver = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )
            logger.info("✅ Connected to remote Chrome")
            return driver
        
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            driver = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )
            logger.info("✅ Connected to remote Firefox")
            return driver
        
        else:
            logger.warning(f"Remote mode only supports Chrome/Firefox, falling back to local for: {browser_name}")
    
    # Local WebDriver (existing code)
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        temp_profile = tempfile.mkdtemp()
        options.add_argument(f'--user-data-dir={temp_profile}')

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "autofill.profile_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
        }
        options.add_experimental_option("prefs", prefs)

        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-save-password-bubble')
        options.add_argument('--disable-features=PasswordManager,PasswordManagerOnboarding')
        options.add_argument('--password-store=basic')

        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)

        is_docker = os.path.exists("/.dockerenv")

        if is_docker:
            options.binary_location = "/usr/bin/chromium"
            options.add_argument("--headless=new")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')

            service = ChromeService(executable_path="/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=options)
            logger.info("Using Chromium in Docker container")
        else:
            for opt in config.CHROME_OPTIONS:
                options.add_argument(opt)
            if config.HEADLESS:
                options.add_argument("--headless=new")

            driver_path = ChromeDriverManager().install()
            driver_path = fix_chromedriver_permissions(driver_path)
            service = ChromeService(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            driver.maximize_window()
            logger.info("Using Chrome locally")

        setattr(driver, "_temp_profile_dir", temp_profile)

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        for opt in config.FIREFOX_OPTIONS:
            options.add_argument(opt)
        if config.HEADLESS:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        if config.HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Edge(options=options)

    elif browser_name == "safari":
        driver = webdriver.Safari()

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    logger.info(f"✅ WebDriver initialized for browser: {browser_name}")
    return driver


# =============================================================================
# ALLURE PARALLEL EXECUTION FIX
# =============================================================================

try:
    from allure_commons.reporter import AllureReporter

    _original_close_test = AllureReporter.close_test

    def safe_close_test(self, uuid):
        try:
            return _original_close_test(self, uuid)
        except KeyError:
            logger.debug(f"Allure: Test {uuid} already closed (parallel execution)")
            return None

    AllureReporter.close_test = safe_close_test
    logger.info("✅ Allure parallel execution patch applied")

except ImportError:
    logger.info("ℹ️ allure-behave not installed - skipping patch")
except Exception as e:
    logger.warning(f"⚠️ Could not apply Allure patch: {e}")
