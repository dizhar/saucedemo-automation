Feature: Checkout Functionality
  As a user of SauceDemo
  I want to complete the checkout process
  So that I can purchase my selected items

  Background:
    Given I am logged in as a standard user

  @smoke @checkout @positive @csv
  Scenario: Complete checkout flow with CSV data
    Given I add "Sauce Labs Backpack" to cart
    And I add "Sauce Labs Bike Light" to cart
    When I view the shopping cart
    And I proceed to checkout
    And I complete checkout with data from CSV "data/checkout_data.csv"
    Then I should see the order confirmation
    And I should see the order complete message

  @checkout @positive
  Scenario: Verify order summary with items and tax calculation
    Given I add "Sauce Labs Backpack" to cart
    And I add "Sauce Labs Bike Light" to cart
    And I add "Sauce Labs Bolt T-Shirt" to cart
    When I view the shopping cart
    And I proceed to checkout
    And I fill in first name "John"
    And I fill in last name "Doe"
    And I fill in postal code "12345"
    And I click continue
    Then I should be on the checkout overview page
    And I should see 3 items in checkout
    And I should verify the order summary calculation
    And I should see the payment information
    And I should see the shipping information
    And I should see the total price

  @checkout @positive
  Scenario: Complete checkout and verify success message
    Given I add "Sauce Labs Backpack" to cart
    When I view the shopping cart
    And I proceed to checkout
    And I fill in first name "John"
    And I fill in last name "Doe"
    And I fill in postal code "12345"
    And I click continue
    And I click finish
    Then I should see the order confirmation
    And I should see the order complete message
    And the page URL should contain "checkout-complete"

  @checkout @negative
  Scenario: Checkout with empty cart should be prevented
    When I view the shopping cart
    Then I should not be able to proceed to checkout
