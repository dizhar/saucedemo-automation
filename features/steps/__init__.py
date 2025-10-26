"""
Behave Step Definitions Package

This package contains all step definitions for the BDD test scenarios.

Step Files:
- login_steps.py: Login and authentication steps
- products_steps.py: Product browsing and sorting steps
- cart_steps.py: Shopping cart management steps
- checkout_steps.py: Checkout process steps
- common_steps.py: Shared/reusable steps across features

Usage:
    Behave automatically discovers all step definitions in this package.
    No manual imports are required.
"""

# This file makes the 'steps' directory a Python package
# Behave will automatically discover all @given, @when, @then decorators
# in any .py files within this directory