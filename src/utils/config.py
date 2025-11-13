"""
Configuration file for SauceDemo test automation project.
Contains all configuration settings, URLs, credentials, and browser configurations.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Main configuration class for test automation"""

    # ==================== PROJECT PATHS ====================
    # Project root directory
    ROOT_DIR = Path(__file__).parent.parent.parent
    
    # Source directories
    SRC_DIR = ROOT_DIR / "src"
    PAGES_DIR = SRC_DIR / "pages"
    UTILS_DIR = SRC_DIR / "utils"
    
    # Test directories
    FEATURES_DIR = ROOT_DIR / "features"
    STEPS_DIR = FEATURES_DIR / "steps"
    
    # Output directories
    REPORTS_DIR = ROOT_DIR / "reports"
    SCREENSHOTS_DIR = ROOT_DIR / "screenshots"
    LOGS_DIR = ROOT_DIR / "logs"
    DRIVERS_DIR = ROOT_DIR / "drivers"

    # ==================== ENVIRONMENT ====================
    # Test environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "test").lower()
    
    # Environments mapping
    ENVIRONMENTS = {
        "dev": "https://dev.saucedemo.com",
        "test": "https://www.saucedemo.com",
        "staging": "https://staging.saucedemo.com",
        "prod": "https://www.saucedemo.com",
    }

    # ==================== APPLICATION URLs ====================
    # BASE_URL is determined by the ENVIRONMENT variable
    BASE_URL = ENVIRONMENTS.get(ENVIRONMENT, "https://www.saucedemo.com")
    LOGIN_URL = f"{BASE_URL}/"
    INVENTORY_URL = f"{BASE_URL}/inventory.html"
    CART_URL = f"{BASE_URL}/cart.html"
    CHECKOUT_STEP_ONE_URL = f"{BASE_URL}/checkout-step-one.html"
    CHECKOUT_STEP_TWO_URL = f"{BASE_URL}/checkout-step-two.html"
    CHECKOUT_COMPLETE_URL = f"{BASE_URL}/checkout-complete.html"

    # ==================== BROWSER CONFIGURATION ====================
    # Default browser
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    
    # Browser options
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    MAXIMIZE_WINDOW = os.getenv("MAXIMIZE_WINDOW", "true").lower() == "true"
    
    # Browser window size (used when not maximized)
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
    
    # Supported browsers
    SUPPORTED_BROWSERS = ["chrome", "firefox", "edge", "safari"]

    # Chrome options
    CHROME_OPTIONS = [
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-notifications",
        "--disable-popup-blocking",
    ]
    
    # Firefox options
    FIREFOX_OPTIONS = [
        "--disable-notifications",
    ]

    # ==================== WAIT TIMEOUTS ====================
    # Default explicit wait timeout (seconds)
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "20"))
    
    # Implicit wait timeout (seconds)
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "20"))
    
    # Page load timeout (seconds)
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "60"))
    
    # Script timeout (seconds)
    SCRIPT_TIMEOUT = int(os.getenv("SCRIPT_TIMEOUT", "30"))
    
    # Short wait (for quick checks)
    SHORT_WAIT = 5
    
    # Long wait (for slow operations)
    LONG_WAIT = 30

    # ==================== SCREENSHOT SETTINGS ====================
    # Take screenshot on failure
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    
    # Take screenshot on success
    SCREENSHOT_ON_SUCCESS = os.getenv("SCREENSHOT_ON_SUCCESS", "false").lower() == "true"
    
    # Screenshot format
    SCREENSHOT_FORMAT = "png"
    
    # Screenshot name pattern
    SCREENSHOT_NAME_PATTERN = "{scenario}_{timestamp}.{format}"

    # ==================== LOGGING SETTINGS ====================
    # Log level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Log format
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Log to file
    LOG_TO_FILE = os.getenv("LOG_TO_FILE", "true").lower() == "true"
    
    # Log to console
    LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"
    
    # Log file name
    LOG_FILE_NAME = "test_automation.log"

    # ==================== REPORTING SETTINGS ====================
    # Report formats
    REPORT_FORMATS = ["html", "json"]
    
    # Allure report
    ALLURE_REPORT = os.getenv("ALLURE_REPORT", "false").lower() == "true"
    ALLURE_RESULTS_DIR = REPORTS_DIR / "allure-results"
    ALLURE_REPORT_DIR = REPORTS_DIR / "allure-reports"
    
    # HTML report
    HTML_REPORT = os.getenv("HTML_REPORT", "true").lower() == "true"
    HTML_REPORT_FILE = REPORTS_DIR / "report.html"
    
    # JSON report
    JSON_REPORT = os.getenv("JSON_REPORT", "true").lower() == "true"
    JSON_REPORT_FILE = REPORTS_DIR / "report.json"

    # ==================== TEST DATA ====================
    # Test checkout data
    TEST_CHECKOUT_DATA = {
        "first_name": "John",
        "last_name": "Doe",
        "postal_code": "12345"
    }
    
    # Invalid credentials for negative testing
    INVALID_CREDENTIALS = {
        "invalid_username": "invalid_user",
        "invalid_password": "invalid_pass",
        "empty_username": "",
        "empty_password": "",
    }

    # ==================== RETRY SETTINGS ====================
    # Retry failed tests
    RETRY_FAILED_TESTS = os.getenv("RETRY_FAILED_TESTS", "false").lower() == "true"
    
    # Number of retries
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))

    # ==================== PARALLEL EXECUTION ====================
    # Run tests in parallel
    PARALLEL_EXECUTION = os.getenv("PARALLEL_EXECUTION", "false").lower() == "true"
    
    # Number of parallel workers
    PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "2"))


    # ==================== BROWSER CONFIGURATION ====================
    # Default browser
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    
    # Browser options
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    MAXIMIZE_WINDOW = os.getenv("MAXIMIZE_WINDOW", "true").lower() == "true"
    
    # Browser window size (used when not maximized)
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
    
    # Remote Selenium Grid (Docker mode)
    SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", None)
    
    # Supported browsers
    SUPPORTED_BROWSERS = ["chrome", "firefox", "edge", "safari"]

    # ==================== HELPER METHODS ====================
    @classmethod
    def get_base_url(cls, environment: Optional[str] = None) -> str:
        """
        Get base URL for specified environment
        
        Args:
            environment: Environment name (dev, test, staging, prod)
            
        Returns:
            str: Base URL
        """
        env = environment or cls.ENVIRONMENT
        return cls.ENVIRONMENTS.get(env, cls.BASE_URL)

    @classmethod
    def create_directories(cls) -> None:
        """Create all necessary directories if they don't exist"""
        directories = [
            cls.REPORTS_DIR,
            cls.SCREENSHOTS_DIR,
            cls.LOGS_DIR,
            cls.DRIVERS_DIR,
            cls.ALLURE_RESULTS_DIR,
            cls.ALLURE_REPORT_DIR,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_browser_options(cls, browser: Optional[str] = None) -> list:
        """
        Get browser-specific options
        
        Args:
            browser: Browser name
            
        Returns:
            list: Browser options
        """
        browser = browser or cls.BROWSER
        
        if browser == "chrome":
            return cls.CHROME_OPTIONS
        elif browser == "firefox":
            return cls.FIREFOX_OPTIONS
        else:
            return []

    @classmethod
    def is_headless(cls) -> bool:
        """
        Check if tests should run in headless mode
        
        Returns:
            bool: True if headless mode enabled
        """
        return cls.HEADLESS

    @classmethod
    def get_screenshot_path(cls, scenario_name: str) -> Path:
        """
        Generate screenshot file path
        
        Args:
            scenario_name: Name of the test scenario
            
        Returns:
            Path: Full path to screenshot file
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{scenario_name}_{timestamp}.{cls.SCREENSHOT_FORMAT}"
        # Sanitize filename
        filename = "".join(c for c in filename if c.isalnum() or c in "._- ")
        return cls.SCREENSHOTS_DIR / filename

    @classmethod
    def get_log_file_path(cls) -> Path:
        """
        Get log file path
        
        Returns:
            Path: Full path to log file
        """
        return cls.LOGS_DIR / cls.LOG_FILE_NAME


# Create an instance for easy access
config = Config()

# Create directories on import
config.create_directories()