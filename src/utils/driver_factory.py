"""
WebDriver Factory
=================
Factory for creating Chrome WebDriver instances (local or remote)
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from .logger import logger


def create_driver():
    """
    Create Chrome WebDriver (local or remote)
    
    Returns:
        WebDriver: Chrome WebDriver instance
    """
    
    chrome_options = Options()
    
    # Check for remote Selenium Grid
    remote_url = os.getenv('SELENIUM_REMOTE_URL')
    
    if remote_url:
        # Remote Selenium Grid (Docker)
        logger.info(f"🌐 Connecting to remote Selenium: {remote_url}")
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Remote(
            command_executor=remote_url,
            options=chrome_options
        )
        
        logger.info("✅ Connected to remote Selenium Grid")
        
    else:
        # Local WebDriver
        logger.info("💻 Using local WebDriver")
        
        # Headless mode
        headless = os.getenv('HEADLESS', 'false').lower() == 'true'
        if headless:
            chrome_options.add_argument('--headless=new')
            logger.info("🔇 Running in headless mode")
        else:
            logger.info("🌐 Running with visible browser")
        
        # Standard options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Additional options for stability
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # ✅ Try Selenium Manager first (built into Selenium 4.6+)
        try:
            driver = webdriver.Chrome(options=chrome_options)
            logger.info("✅ Local WebDriver created via Selenium Manager")
        except Exception as e:
            logger.warning(f"Selenium Manager failed ({e}); falling back to webdriver_manager")
            driver_path = ChromeDriverManager().install()
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("✅ Local WebDriver created via webdriver_manager fallback")
    
    # Set implicit wait
    implicit_wait = int(os.getenv('IMPLICIT_WAIT', '10'))
    driver.implicitly_wait(implicit_wait)
    
    # Maximize window if configured
    if os.getenv('MAXIMIZE_WINDOW', 'true').lower() == 'true':
        driver.maximize_window()
        logger.info("🖥️ Browser window maximized")
    
    return driver


def get_driver_capabilities(driver):
    """
    Get driver capabilities info
    
    Args:
        driver: WebDriver instance
        
    Returns:
        dict: Driver capabilities
    """
    try:
        caps = driver.capabilities
        return {
            'browser': caps.get('browserName', 'unknown'),
            'version': caps.get('browserVersion', 'unknown'),
            'platform': caps.get('platformName', 'unknown')
        }
    except Exception as e:
        logger.warning(f"Could not retrieve driver capabilities: {e}")
        return {}
