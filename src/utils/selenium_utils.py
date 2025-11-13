# /Users/danielizhar/dev/saucedemo-automation/src/utils/selenium_utils.py
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

CHROME_BIN = os.environ.get("CHROME_BIN", "/usr/bin/chromium")
CHROMEDRIVER = os.environ.get("CHROMEDRIVER", "/usr/bin/chromedriver")

# Prefer SELENIUM_REMOTE_URL, fallback to GRID_URL for compatibility
REMOTE_URL = os.environ.get("SELENIUM_REMOTE_URL") or os.environ.get("GRID_URL")

def make_driver(window_size: str = "1920,1080"):
    opts = Options()
    opts.binary_location = CHROME_BIN
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument(f"--window-size={window_size}")

    if REMOTE_URL:
        return webdriver.Remote(command_executor=REMOTE_URL, options=opts)

    service = Service(executable_path=CHROMEDRIVER)
    return webdriver.Chrome(service=service, options=opts)
