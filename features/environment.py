"""
Behave environment setup and teardown hooks.
"""

from datetime import datetime
import os
import warnings
import tempfile
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


def before_all(context):
    """
    Runs once before all tests
    
    Args:
        context: Behave context object
    """
    logger.info("=" * 80)
    logger.info("Starting Test Execution")
    logger.info("=" * 80)
    
    # Create necessary directories
    config.create_directories()


def before_scenario(context, scenario):
    """
    Runs before each scenario
    
    Args:
        context: Behave context object
        scenario: Current scenario
    """
    logger.info(f"Starting Scenario: {scenario.name}")
    
    # Initialize browser
    context.driver = get_driver(config.BROWSER)
    
    # Set timeouts
    context.driver.implicitly_wait(config.IMPLICIT_WAIT)
    context.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
    context.driver.set_script_timeout(config.SCRIPT_TIMEOUT)
    
    # Maximize window if configured
    if config.MAXIMIZE_WINDOW:
        context.driver.maximize_window()
    else:
        context.driver.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    
    logger.info(f"Browser initialized: {config.BROWSER}")


def after_scenario(context, scenario):
    """
    Cleanup after each scenario
    """
    try:
        # Only take screenshot if driver exists and scenario failed
        if hasattr(context, 'driver') and scenario.status.name == "failed":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"failed_{scenario.name}_{timestamp}.png"
            screenshot_path = os.path.join("screenshots", screenshot_name)
            
            os.makedirs("screenshots", exist_ok=True)
            context.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        logger.error(f"Error taking screenshot: {str(e)}")
    finally:
        if hasattr(context, 'driver'):
            context.driver.quit()
            logger.info("Browser closed")


def after_all(_context):
    """
    Runs once after all tests
    """
    logger.info("=" * 80)
    logger.info("Test Execution Completed")
    logger.info("=" * 80)


def fix_chromedriver_permissions(driver_path):
    """
    Fix ChromeDriver permissions issue on Mac.
    webdriver-manager sometimes sets wrong permissions.
    
    Args:
        driver_path: Path returned by ChromeDriverManager
        
    Returns:
        Corrected path to chromedriver executable
    """
    driver_dir = os.path.dirname(driver_path)
    chromedriver_file = os.path.join(driver_dir, "chromedriver")
    
    # Make sure chromedriver is executable
    if os.path.exists(chromedriver_file):
        try:
            os.chmod(chromedriver_file, 0o755)
            logger.info(f"Fixed permissions for: {chromedriver_file}")
            return chromedriver_file
        except Exception as e:
            logger.warning(f"Could not fix permissions: {e}")
    
    return driver_path


def get_driver(browser_name: str):
    """
    Initialize and return WebDriver based on browser name
    
    Args:
        browser_name: Name of browser (chrome, firefox, edge, safari)
        
    Returns:
        WebDriver instance
    """
    browser_name = browser_name.lower()
    
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        
        # Use temporary profile to avoid saved passwords and popups
        temp_profile = tempfile.mkdtemp()
        options.add_argument(f'--user-data-dir={temp_profile}')
        
        # COMPREHENSIVE FIX: Disable password manager and autofill
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "autofill.profile_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
        }
        options.add_experimental_option("prefs", prefs)
        
        # Additional Chrome arguments to disable password features
        temp_profile = tempfile.mkdtemp()
        
        options.add_argument(f'--user-data-dir={temp_profile}')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-save-password-bubble')
        options.add_argument('--disable-features=PasswordManager,PasswordManagerOnboarding')
        options.add_argument('--password-store=basic')
            
        # Disable automation detection
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Check if running in Docker (Chromium) or locally (Chrome)
        is_docker = os.path.exists("/.dockerenv")
        
        if is_docker:
            # Use Chromium in Docker
            options.binary_location = "/usr/bin/chromium"
            
            # Docker-specific options
            options.add_argument("--headless=new") 
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            # Headless mode for Docker
            options.add_argument("--headless=new")
            
            # Use system chromium-driver
            service = ChromeService(executable_path="/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=options)
            logger.info("Using Chromium in Docker container")
        else:
            # Use Chrome locally (your Mac setup)
            for option in config.CHROME_OPTIONS:
                options.add_argument(option)
            
            if config.HEADLESS:
                options.add_argument("--headless=new")
            
            # Use webdriver-manager and fix permissions (for local Mac)
            driver_path = ChromeDriverManager().install()
            driver_path = fix_chromedriver_permissions(driver_path)
            
            service = ChromeService(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            logger.info("Using Chrome locally")
        
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        
        # Add firefox options
        for option in config.FIREFOX_OPTIONS:
            options.add_argument(option)
        
        # Headless mode
        if config.HEADLESS:
            options.add_argument("--headless")
        
        # Use webdriver-manager to auto-download geckodriver
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
    
    logger.info(f"WebDriver initialized for browser: {browser_name}")
    return driver


# =============================================================================
# ALLURE PARALLEL EXECUTION FIX
# =============================================================================
# When running tests in parallel with allure-behave, a KeyError occurs during
# test cleanup because multiple processes try to close the same test UUID.
# This patch wraps the close_test method to handle KeyError gracefully,
# allowing all test results to be written successfully.
# =============================================================================

try:
    from allure_commons.reporter import AllureReporter
    
    # Store the original close_test method
    _original_close_test = AllureReporter.close_test
    
    def safe_close_test(self, uuid):
        """Close test, handling KeyError gracefully for parallel execution."""
        try:
            return _original_close_test(self, uuid)
        except KeyError:
            # Test UUID already cleaned up by another process
            # This is expected in parallel execution - results are already written
            logger.debug(f"Allure: Test {uuid} already closed (parallel execution)")
            return None
    
    # Replace the close_test method
    AllureReporter.close_test = safe_close_test
    
    logger.info("✅ Allure parallel execution patch applied")

except ImportError:
    logger.info("ℹ️  allure-behave not installed - skipping patch")
except Exception as e:
    logger.warning(f"⚠️  Could not apply Allure patch: {e}")