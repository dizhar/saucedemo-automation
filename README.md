# 🛒 SauceDemo Test Automation Framework

A comprehensive BDD (Behavior-Driven Development) test automation framework for [SauceDemo](https://www.saucedemo.com/) e-commerce application using Python, Behave, Selenium, and Allure reporting.

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.x-green.svg)](https://selenium.dev/)
[![Behave](https://img.shields.io/badge/behave-1.2.6-orange.svg)](https://behave.readthedocs.io/)
[![Allure](https://img.shields.io/badge/allure-2.x-yellow.svg)](https://docs.qameta.io/allure/)

---

## ⚡ Quick Start

Get up and running in 5 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/saucedemo-automation.git
cd saucedemo-automation

# 2. Install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env

# 4. Run tests with Docker (Recommended - includes parallel execution + reports)
./run_docker_tests.sh

# OR run tests locally
behave -f pretty
```

**With Docker (Fastest):**

```bash
# One command to run all tests in parallel with beautiful reports
./run_docker_tests.sh --workers 8
```

**View Test Reports:**

```bash
# Open the latest report
./open_report.sh
```

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running Tests](#-running-tests)
- [Docker Support](#-docker-support)
- [Parallel Test Execution](#-parallel-test-execution)
- [Test Reports](#-test-reports)
- [Test Coverage](#-test-coverage)
- [Writing Tests](#-writing-tests)
- [Helper Scripts](#-helper-scripts)
- [CI/CD Integration](#-cicd-integration)
- [Troubleshooting](#-troubleshooting)
- [Best Practices](#-best-practices)
- [Contributing](#-contributing)

---

## ✨ Features

- 🎯 **BDD Framework**: Gherkin syntax with Behave for readable test scenarios
- 🌐 **Multi-Browser Support**: Chrome, Firefox, Edge, Safari
- 📊 **Allure Reports**: Beautiful, interactive test reports with screenshots
- 📸 **Auto Screenshots**: Captures screenshots on test failures
- 📝 **Comprehensive Logging**: Detailed logs for debugging
- 🔧 **Page Object Model**: Maintainable and scalable test architecture
- ⚙️ **Environment Configuration**: Easy configuration via `.env` file
- 🏷️ **Tag-Based Execution**: Run specific test suites (@smoke, @regression, etc.)
- 🚀 **WebDriver Manager**: Auto-downloads and manages browser drivers
- 🔄 **Parallel Execution**: Built-in parallel test runner for faster execution
- 🐳 **Docker Support**: Fully containerized testing with automated reporting
- 🎬 **One-Command Execution**: Complete test run + report generation with single script

---

## 📁 Project Structure

```
saucedemo-automation/
├── features/                      # BDD feature files
│   ├── environment.py            # Behave hooks (setup/teardown)
│   ├── steps/                    # Step definitions
│   │   ├── __init__.py
│   │   ├── login_steps.py       # Login step definitions
│   │   ├── products_steps.py    # Products step definitions
│   │   ├── cart_steps.py        # Cart step definitions
│   │   ├── checkout_steps.py    # Checkout step definitions
│   │   └── common_steps.py      # Shared step definitions
│   ├── login.feature            # Login test scenarios (20 tests)
│   ├── products.feature         # Products test scenarios (41 tests)
│   ├── cart.feature             # Cart test scenarios (32 tests)
│   └── checkout.feature         # Checkout test scenarios (32 tests)
│
├── src/                          # Source code
│   ├── pages/                   # Page Object Models
│   │   ├── __init__.py
│   │   ├── base_page.py        # Base page class
│   │   ├── login_page.py       # Login page object
│   │   └── products_page.py    # Products page object
│   └── utils/                   # Utility modules
│       ├── __init__.py
│       ├── config.py           # Configuration management
│       └── logger.py           # Logging setup
│
├── reports/                     # Test reports
│   ├── allure-results/         # Allure test results (raw)
│   ├── allure-results-merged/  # Merged parallel test results
│   └── allure-report/          # Generated HTML reports
│
├── screenshots/                 # Test failure screenshots
├── logs/                        # Test execution logs
├── .env                         # Environment configuration
├── .env.example                 # Example environment file
├── behave.ini                   # Behave configuration
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image configuration
├── docker-compose.yml           # Docker Compose configuration
├── .dockerignore               # Docker ignore rules
├── test_runner.py              # Parallel test execution script
├── run_docker_tests.sh         # Docker test runner with reporting
├── open_report.sh              # Open Allure reports easily
├── .gitignore                   # Git ignore rules
├── pyrightconfig.json          # Pylance configuration
└── README.md                    # This file
```

---

## 🔧 Prerequisites

- **Python**: 3.9 or higher
- **pip**: Python package manager
- **Git**: Version control
- **Browser**: Chrome, Firefox, Edge, or Safari
- **Java**: JDK 8+ (for Allure reports)
- **Allure Command Line**: For viewing reports

### Install Prerequisites (macOS)

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python@3.11

# Install Java (for Allure)
brew install openjdk@11

# Install Allure
brew install allure
```

### Install Prerequisites (Windows)

```bash
# Install Chocolatey (if not installed)
# Run in PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python
choco install python

# Install Java
choco install openjdk11

# Install Allure
choco install allure
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/saucedemo-automation.git
cd saucedemo-automation
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your configuration
nano .env  # or use your preferred editor
```

---

## ⚙️ Configuration

Edit the `.env` file to customize your test execution:

```bash
# Browser Configuration
BROWSER=chrome                    # chrome, firefox, edge, safari
HEADLESS=false                    # Run browser in headless mode

# Window Configuration
MAXIMIZE_WINDOW=true              # Maximize browser window
WINDOW_WIDTH=1920                 # Window width (if not maximized)
WINDOW_HEIGHT=1080                # Window height (if not maximized)

# Timeout Configuration
IMPLICIT_WAIT=10                  # Implicit wait in seconds
PAGE_LOAD_TIMEOUT=30              # Page load timeout
SCRIPT_TIMEOUT=30                 # Script execution timeout

# Screenshot Configuration
SCREENSHOT_ON_FAILURE=true        # Capture screenshot on failure
SCREENSHOT_ON_SUCCESS=false       # Capture screenshot on success

# Directories
LOG_LEVEL=info

ENVIRONMENT=test                 # dev, test, staging, prod
```

---

## 🏃 Running Tests

### Run Tests Locally (Recommended)

Run tests with pretty formatting for better readability:

```bash
# Run all tests with pretty format
behave -f pretty

# Run specific feature with pretty format
behave features/login.feature -f pretty

# Run smoke tests with pretty format
behave --tags=@smoke -f pretty
```

### Run Tests in Headless Mode

To run tests without opening a visible browser window:

**Option 1: Using Environment Variable**

```bash
# Set headless mode in .env file
HEADLESS=true

# Then run tests normally
behave -f pretty
```

**Option 2: Using Command Line**

```bash
# Export environment variable (macOS/Linux)
export HEADLESS=true
behave -f pretty

# Set for single run (macOS/Linux)
HEADLESS=true behave -f pretty

# PowerShell (Windows)
$env:HEADLESS="true"
behave -f pretty

# CMD (Windows)
set HEADLESS=true
behave -f pretty
```

### Run All Tests

```bash
behave
```

### Run Specific Feature

```bash
behave features/login.feature
behave features/cart.feature
behave features/products.feature
behave features/checkout.feature
```

### Run by Tags

```bash
# Run smoke tests only
behave --tags=@smoke

# Run positive tests
behave --tags=@positive

# Run negative tests
behave --tags=@negative

# Run specific feature tests
behave --tags=@login
behave --tags=@cart
behave --tags=@checkout

# Run workflow tests
behave --tags=@workflow

# Exclude specific tags
behave --tags="not @slow"

# Combine tags (AND)
behave --tags=@smoke --tags=@login

# Combine tags (OR)
behave --tags=@smoke,@regression
```

### Run with Options

```bash
# Dry run (syntax check)
behave --dry-run

# Stop on first failure
behave --stop

# Run parallel (requires behave-parallel)
behave --processes 4 --parallel-element feature

# Verbose output
behave --verbose
```

### Run Specific Scenario

```bash
# By line number
behave features/login.feature:10

# By name pattern
behave --name "successful login"
```

---

## 🐳 Docker Support

### Quick Start with Docker Script (Recommended)

The easiest way to run tests in Docker with parallel execution and automatic Allure report generation:

```bash
# Run tests with default settings (4 workers, auto-open report)
./run_docker_tests.sh

# Run with custom number of workers
./run_docker_tests.sh --workers 8

# Run without automatically opening the report
./run_docker_tests.sh --no-open

# Run without cleaning previous reports
./run_docker_tests.sh --no-clean

# Combine options
./run_docker_tests.sh --workers 6 --no-open
```

The script will:

- 🔨 Build the Docker image
- 🧪 Run tests in parallel (default: 4 workers)
- 📊 Merge results from parallel workers
- 📈 Generate beautiful Allure reports
- 🌐 Automatically open the report in your browser

### Build Docker Image

```bash
# Build the Docker image
docker build -t saucedemo-tests .
```

### Run Tests in Docker (Manual)

```bash
# Run all tests in Docker container
docker run --rm saucedemo-tests

# Run with pretty format
docker run --rm saucedemo-tests behave -f pretty

# Run smoke tests only
docker run --rm saucedemo-tests behave --tags=@smoke -f pretty

# Run in headless mode (default in Docker)
docker run --rm -e HEADLESS=true saucedemo-tests

# Run with volume mounts to access reports
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  -v $(pwd)/screenshots:/app/screenshots \
  -v $(pwd)/logs:/app/logs \
  saucedemo-tests behave -f pretty
```

### Docker Compose

```bash
# Run tests using Docker Compose
docker-compose up --build

# Run and remove containers after
docker-compose up --build --abort-on-container-exit

# Run specific service
docker-compose run saucedemo-tests behave --tags=@smoke -f pretty
```

---

## 🚀 Parallel Test Execution

The framework includes a powerful parallel test runner (`test_runner.py`) for faster execution:

### Run Tests in Parallel (Local)

```bash
# Run all features in parallel with 4 workers (default)
python test_runner.py --workers 4 --report

# Run with 8 parallel workers
python test_runner.py --workers 8 --report

# Run scenarios in parallel (finer granularity)
python test_runner.py --mode scenarios --workers 8 --report

# Run specific feature file's scenarios in parallel
python test_runner.py --mode scenarios --file features/products.feature --workers 4 --report

# Generate and serve report in browser immediately
python test_runner.py --workers 4 --serve

# Clean previous results before running
python test_runner.py --workers 4 --report --clean
```

### Parallel Execution Options

- `--mode features`: Run entire feature files in parallel (default, faster for fewer large features)
- `--mode scenarios`: Run individual scenarios in parallel (better for many small scenarios)
- `--workers N`: Number of parallel workers (default: 4)
- `--report`: Generate Allure report after tests
- `--serve`: Generate and open report in browser
- `--clean`: Clean previous results before running
- `--file`: Specific feature file (use with `--mode scenarios`)

### Benefits of Parallel Execution

- ⚡ **Faster Execution**: Run 125+ tests in minutes instead of hours
- 🔄 **Better Resource Usage**: Utilize all CPU cores
- 📊 **Automatic Merging**: Results from all workers are automatically merged
- 🎯 **Flexible Granularity**: Run by features or individual scenarios

---

## 📊 Test Reports

### Quick View Report (Recommended)

```bash
# Open the latest generated report
./open_report.sh
```

This script will:

- ✅ Check if report exists
- 🚀 Open with Allure CLI (if installed)
- 🌐 Or start a local web server and open in browser
- 🔧 Handle port conflicts automatically

### Generate and View Allure Report

```bash
# Run tests (generates allure-results)
behave -f pretty

# Generate and open interactive Allure report
allure serve reports/allure-results

# Or generate static HTML report
allure generate reports/allure-results --clean -o reports/allure-report
allure open reports/allure-report
```

### Generate HTML Report (Optional)

Behave can generate basic HTML reports using the `behave-html-formatter` plugin:

**Install HTML Formatter:**

```bash
pip install behave-html-formatter
```

**Generate HTML Report:**

```bash
# Run tests and generate HTML report
behave -f html -o reports/test-report.html

# Run with both pretty console output and HTML report
behave -f pretty -f html -o reports/test-report.html

# Open the report in browser (macOS)
open reports/test-report.html

# Open the report in browser (Linux)
xdg-open reports/test-report.html

# Open the report in browser (Windows)
start reports/test-report.html
```

**Alternative: Allure HTML Report (Recommended)**

```bash
# Generate standalone HTML report with Allure
allure generate reports/allure-results --clean -o reports/allure-html-report

# The report is in reports/allure-html-report/index.html
# Open it in any web browser
open reports/allure-html-report/index.html  # macOS
```

### Allure Report Features

- ✅ Test execution overview
- ✅ Test history trends
- ✅ Categories and suites
- ✅ Failure screenshots
- ✅ Test duration statistics
- ✅ Environment information
- ✅ Tags and behaviors

### View Logs

```bash
# View latest test execution log
tail -f logs/test_execution.log

# View with grep
grep "ERROR" logs/test_execution.log
grep "Failed" logs/test_execution.log
```

---

## 📈 Test Coverage

### Test Statistics

| Feature      | Scenarios | Test Cases | Coverage                       |
| ------------ | --------- | ---------- | ------------------------------ |
| **Login**    | 11        | ~20        | Authentication, Error handling |
| **Products** | 29        | ~41        | Browsing, Sorting, Navigation  |
| **Cart**     | 21        | ~32        | Add/Remove, Badge, Persistence |
| **Checkout** | 21        | ~32        | Form validation, Order flow    |
| **TOTAL**    | **82**    | **~125**   | **End-to-End Coverage**        |

### Test Categories

- 🟢 **Smoke Tests** (8 scenarios): Critical path validation
- 🟢 **Positive Tests** (60+ scenarios): Happy path scenarios
- 🔴 **Negative Tests** (15+ scenarios): Error handling and validation
- 🔵 **Workflow Tests** (4 scenarios): End-to-end user journeys
- 🟡 **Integration Tests** (5 scenarios): Cross-feature testing
- ⚠️ **Edge Cases** (8 scenarios): Boundary conditions

---

## ✍️ Writing Tests

### Create a New Feature File

```gherkin
# features/new_feature.feature
Feature: New Feature Name
  As a user
  I want to perform some action
  So that I can achieve some goal

  Background:
    Given I am logged in as a standard user

  @smoke @new_feature
  Scenario: Basic scenario
    When I perform some action
    Then I should see expected result

  @new_feature
  Scenario Outline: Data-driven test
    When I perform action with "<input>"
    Then I should see "<output>"

    Examples:
      | input  | output  |
      | value1 | result1 |
      | value2 | result2 |
```

### Create Step Definitions

```python
# features/steps/new_feature_steps.py
from behave import given, when, then
from src.utils.logger import logger

@when('I perform some action')
def step_perform_action(context):
    """Perform some action"""
    # Your implementation here
    logger.info("Performing action")

@then('I should see expected result')
def step_verify_result(context):
    """Verify expected result"""
    # Your assertions here
    assert True, "Expected result not found"
    logger.info("Verified expected result")
```

### Create Page Object

```python
# src/pages/new_page.py
from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class NewPage(BasePage):
    """Page object for new page"""

    # Locators
    ELEMENT_LOCATOR = (By.ID, "element-id")

    def __init__(self, driver):
        super().__init__(driver)

    def perform_action(self):
        """Perform action on page"""
        self.click(self.ELEMENT_LOCATOR)

    def get_text(self):
        """Get text from element"""
        return self.get_element_text(self.ELEMENT_LOCATOR)
```

---

## 🛠️ Helper Scripts

The framework includes several helper scripts for easier workflow:

### 1. `run_docker_tests.sh`

Complete Docker-based test execution with parallel processing and automatic reporting.

**Features:**

- Automatically builds Docker image
- Runs tests in parallel (configurable workers)
- Merges results from parallel workers
- Generates Allure reports
- Opens report in browser

**Usage:**

```bash
./run_docker_tests.sh --help
./run_docker_tests.sh --workers 8
./run_docker_tests.sh --no-open
./run_docker_tests.sh --workers 6 --no-clean
```

### 2. `open_report.sh`

Quick report viewer that works with or without Allure CLI.

**Features:**

- Checks if report exists
- Opens with Allure CLI (preferred)
- Falls back to Python HTTP server
- Handles port conflicts
- Works on macOS, Linux, and Windows (Git Bash)

**Usage:**

```bash
./open_report.sh
```

### 3. `test_runner.py`

Python-based parallel test runner for local development.

**Features:**

- Run tests by features or scenarios
- Configurable parallel workers
- Automatic result merging
- Allure report generation
- Clean previous results option

**Usage:**

```bash
python test_runner.py --help
python test_runner.py --workers 8 --report
python test_runner.py --mode scenarios --serve
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. WebDriver Issues

```bash
# Issue: ChromeDriver version mismatch
# Solution: webdriver-manager handles this automatically
pip install --upgrade webdriver-manager
```

#### 2. Import Errors

```bash
# Issue: Module not found
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Behave Not Finding Steps

```bash
# Issue: Steps not discovered
# Solution: Check step definitions syntax
behave --dry-run  # Verify step matching
```

#### 4. Allure Report Issues

```bash
# Issue: Allure command not found
# Solution: Install Allure
brew install allure  # macOS
choco install allure # Windows

# Linux (Debian/Ubuntu)
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

#### 5. Docker Issues

```bash
# Issue: Docker build fails
# Solution: Clean Docker cache and rebuild
docker system prune -a
docker build --no-cache -t saucedemo-tests .

# Issue: Permission denied on scripts
# Solution: Make scripts executable
chmod +x run_docker_tests.sh open_report.sh

# Issue: Port already in use
# Solution: Kill the process or use different port
lsof -ti:8080 | xargs kill -9

# Issue: Volume mount not working
# Solution: Use absolute paths
docker run -v $(pwd)/reports:/app/reports saucedemo-tests
```

#### 6. Parallel Execution Issues

```bash
# Issue: Tests fail in parallel but pass individually
# Solution: Check for test dependencies or shared state
# Ensure tests are independent and don't share data

# Issue: Allure results not merging
# Solution: Check directory structure
ls -la reports/allure-results/
# Should see subdirectories with PID names containing .json files

# Issue: Out of memory with too many workers
# Solution: Reduce number of workers
python test_runner.py --workers 2 --report
# Or
./run_docker_tests.sh --workers 2
```

#### 7. Report Generation Issues

```bash
# Issue: Empty or incomplete reports
# Solution: Verify test results exist
ls -la reports/allure-results-merged/
# Should contain .json files

# Regenerate report manually
allure generate reports/allure-results-merged --clean -o reports/allure-report

# Issue: Report won't open
# Solution: Use the helper script
./open_report.sh

# Or manually serve with Python
cd reports/allure-report
python3 -m http.server 8080
```

#### 8. Environment Variable Issues

```bash
# Issue: .env file not being read
# Solution: Ensure .env file exists in project root
cp .env.example .env

# Verify environment variables
python -c "from src.utils.config import Config; print(Config.BROWSER)"

# Issue: HEADLESS mode not working
# Solution: Set explicitly
export HEADLESS=true  # macOS/Linux
set HEADLESS=true     # Windows CMD
$env:HEADLESS="true"  # Windows PowerShell
```

---

## 🎯 Best Practices

### 1. Test Organization

- ✅ Keep feature files focused on single functionality
- ✅ Use Background for common setup steps
- ✅ Tag scenarios appropriately (@smoke, @regression)
- ✅ Write descriptive scenario names

### 2. Step Definitions

- ✅ Keep steps reusable and atomic
- ✅ Use meaningful parameter names
- ✅ Add proper logging to steps
- ✅ Handle waits properly (implicit/explicit)

### 3. Page Objects

- ✅ One page object per page
- ✅ Use clear locator naming
- ✅ Encapsulate page interactions
- ✅ Avoid assertions in page objects

### 4. Code Quality

- ✅ Follow PEP 8 style guide
- ✅ Write docstrings for functions
- ✅ Use type hints where appropriate
- ✅ Keep functions small and focused

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   behave --tags=@smoke
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- [SauceDemo](https://www.saucedemo.com/) - Test application
- [Behave](https://behave.readthedocs.io/) - BDD framework
- [Selenium](https://selenium.dev/) - Browser automation
- [Allure](https://docs.qameta.io/allure/) - Test reporting

---

## 📚 Additional Resources

- **Test Scripts**: All helper scripts are in the project root

  - [`run_docker_tests.sh`](run_docker_tests.sh) - Complete Docker test automation
  - [`open_report.sh`](open_report.sh) - Quick report viewer
  - [`test_runner.py`](test_runner.py) - Parallel test runner

- **Test Documentation**:

  - [`manual_test_cases.docx`](manual_test_cases.docx) - Manual test cases documentation

- **Documentation**:

  - [Behave Documentation](https://behave.readthedocs.io/)
  - [Selenium Documentation](https://selenium.dev/documentation/)
  - [Allure Framework](https://docs.qameta.io/allure/)
  - [Docker Documentation](https://docs.docker.com/)

- **Project Files**:
  - [`.env.example`](.env.example) - Environment configuration template
  - [`behave.ini`](behave.ini) - Behave framework settings
  - [`Dockerfile`](Dockerfile) - Docker image configuration
  - [`docker-compose.yml`](docker-compose.yml) - Docker Compose setup

---

## 🎯 Summary

This framework provides:

✅ **Complete BDD Testing Solution** - 125+ tests covering full e-commerce workflow
✅ **Parallel Execution** - Run tests 4-8x faster with built-in parallel runner
✅ **Docker Support** - One-command execution with `./run_docker_tests.sh`
✅ **Beautiful Reports** - Interactive Allure reports with screenshots
✅ **Easy to Use** - Helper scripts for common tasks
✅ **CI/CD Ready** - GitHub Actions and Jenkins examples included
✅ **Well Documented** - Comprehensive README and inline documentation

**Get Started in 30 Seconds:**

```bash
./run_docker_tests.sh  # That's it!
```

---

**⭐ Star this repository if you find it helpful!**

---

_Last Updated: October 2024_
