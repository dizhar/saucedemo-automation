Feature: Shopping Cart Functionality
  As a user of SauceDemo
  I want to manage items in my shopping cart
  So that I can purchase the products I want

  Background:
    Given I am logged in as a standard user

  @smoke @cart @positive
  Scenario: Add multiple items to cart
    When I add "Sauce Labs Backpack" to cart
    And I add "Sauce Labs Bike Light" to cart
    And I add "Sauce Labs Bolt T-Shirt" to cart
    Then the cart should contain 3 items
    And the cart badge should display 3

  @cart @positive
  Scenario: Cart badge increments correctly
    When I add "Sauce Labs Backpack" to cart
    Then the cart badge should display 1
    When I add "Sauce Labs Bike Light" to cart
    Then the cart badge should display 2
    When I add "Sauce Labs Bolt T-Shirt" to cart
    Then the cart badge should display 3

  @cart @positive
  Scenario: Remove item from cart with multiple items
    Given I add "Sauce Labs Backpack" to cart
    And I add "Sauce Labs Bike Light" to cart
    And I add "Sauce Labs Bolt T-Shirt" to cart
    When I remove "Sauce Labs Bike Light" from cart
    Then the cart should contain 2 items
    And the cart badge should display 2
    And "Sauce Labs Bike Light" should not be in the cart

  @cart @workflow
  Scenario: Complete shopping cart workflow
    # Start with empty cart
    Then the cart should be empty
    
    # Add 3 items
    When I add "Sauce Labs Backpack" to cart
    And I add "Sauce Labs Bike Light" to cart
    And I add "Sauce Labs Bolt T-Shirt" to cart
    Then the cart should contain 3 items
    
    # Remove one item
    When I remove "Sauce Labs Bike Light" from cart
    Then the cart should contain 2 items
    
    # View cart
    When I view the shopping cart
    Then the page URL should contain "cart.html"
    
    # Cart should still have 2 items
    And the cart badge should display 2