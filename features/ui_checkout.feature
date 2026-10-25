Feature: SauceDemo UI checkout flow

  Background:
    Given the browser is launched
    And the user is on the login page

  Scenario: Successful checkout of a single item
    When I login with username "standard_user" and password "secret_sauce"
    And I add the product "Sauce Labs Backpack" to the cart
    And I proceed to the checkout page
    And I fill in checkout information
    Then the order confirmation page is displayed
    And the visual AI check for the confirmation page passes