Feature: Login Functionality (Data-Driven with users.json
  As a user of SauceDemo
  I want to login with credentials from users.json
  So that test data is centrally managed and maintainable

  Background:
    Given I am on the login page

  # ==================== POSITIVE LOGIN TESTS ====================

  @smoke @login @positive @data-driven
  Scenario: Successful login with standard user from users.json
    When I login with valid user "standard_user"
    Then I should be on the products page
    And I should see the app logo

  @smoke @login @positive @data-driven
  Scenario Outline: Successful login with different valid users from users.json
    When I login with valid user "<user_type>"
    Then I should be on the products page
    And I should see the app logo

    Examples:
      | user_type               |
      | standard_user           |
      | problem_user            |
      | performance_glitch_user |
      | error_user              |
      | visual_user             |

  # ==================== NEGATIVE LOGIN TESTS - LOCKED USER ====================

  @smoke @login @negative @locked @data-driven
  Scenario: Login fails for locked out user from users.json
    When I login with locked user
    Then I should see the expected error for "locked"
    And I should remain on the login page

  # ==================== NEGATIVE LOGIN TESTS - INVALID CREDENTIALS ====================

  @smoke @login @negative @data-driven
  Scenario: Login fails with invalid username from users.json
    When I login with invalid credentials case "invalid_username"
    Then I should see the expected error for "invalid_username"
    And I should remain on the login page

  @smoke @login @negative @data-driven
  Scenario: Login fails with invalid password from users.json
    When I login with invalid credentials case "invalid_password"
    Then I should see the expected error for "invalid_password"
    And I should remain on the login page

  @smoke @login @negative @data-driven
  Scenario: Login fails with both invalid credentials from users.json
    When I login with invalid credentials case "both_invalid"
    Then I should see the expected error for "both_invalid"
    And I should remain on the login page

  @smoke @login @negative @data-driven
  Scenario Outline: Login fails with invalid credentials from users.json
    When I login with invalid credentials case "<case_type>"
    Then I should see the expected error for "<error_type>"
    And I should remain on the login page

    Examples:
      | case_type        | error_type       |
      | invalid_username | invalid_username |
      | invalid_password | invalid_password |
      | both_invalid     | both_invalid     |

  # ==================== NEGATIVE LOGIN TESTS - EMPTY FIELDS ====================

  @smoke @login @negative @validation @data-driven
  Scenario: Login fails with empty username from users.json
    When I login with empty credentials case "empty_username"
    Then I should see the expected error for "empty_username"
    And I should remain on the login page

  @smoke @login @negative @validation @data-driven
  Scenario: Login fails with empty password from users.json
    When I login with empty credentials case "empty_password"
    Then I should see the expected error for "empty_password"
    And I should remain on the login page

  @smoke @login @negative @validation @data-driven
  Scenario: Login fails with empty username and password from users.json
    When I login with empty credentials case "both_empty"
    Then I should see the expected error for "empty_username"
    And I should remain on the login page

  @smoke @login @negative @validation @data-driven
  Scenario Outline: Login fails with empty credentials from users.json
    When I login with empty credentials case "<case_type>"
    Then I should see the expected error for "<error_type>"
    And I should remain on the login page

    Examples:
      | case_type      | error_type     |
      | empty_username | empty_username |
      | empty_password | empty_password |
      | both_empty     | empty_username |

  # ==================== WORKFLOW TESTS ====================

  @login @workflow @data-driven
  Scenario: Complete login and logout workflow using users.json
    When I login with valid user "standard_user"
    Then I should be on the products page
    When I open the menu
    And I click logout
    Then the page URL should contain "https://www.saucedemo.com/"

  @login @workflow @data-driven
  Scenario: Attempt login with invalid credentials then succeed with valid ones from users.json
    When I login with invalid credentials case "both_invalid"
    Then I should see an error message
    And I should remain on the login page
    When I login with valid user "standard_user"
    Then I should be on the products page
    And I should see the app logo

  @login @workflow @data-driven
  Scenario: Multiple failed login attempts then success from users.json
    When I login with invalid credentials case "invalid_username"
    Then I should see an error message
    When I login with invalid credentials case "invalid_password"
    Then I should see an error message
    When I login with locked user
    Then I should see an error message
    When I login with valid user "standard_user"
    Then I should be on the products page
