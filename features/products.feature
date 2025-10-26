Feature: Products Page Functionality
  As a user of SauceDemo
  I want to browse and sort products
  So that I can find and select items I want to purchase

  Background:
    Given I am logged in as a standard user

  @smoke @products @positive
  Scenario: Verify products page loads successfully
    Then I should be on the products page
    And I should see 6 products
    And I should see the app logo

  @smoke @products @positive
  Scenario: Verify all products are displayed
    Then I should see 6 products

  @smoke @products @positive
  Scenario: Verify all product names are not empty
    Then all product names should not be empty

  @smoke @products @positive
  Scenario: Verify all product prices are greater than zero
    Then all product prices should be greater than 0

  @smoke @products @positive
  Scenario: Sort products by price low to high
    When I sort products by "Price (low to high)"
    Then the products should be sorted by price low to high

  @products @positive
  Scenario: Sort products by price high to low
    When I sort products by "Price (high to low)"
    Then the products should be sorted by price high to low