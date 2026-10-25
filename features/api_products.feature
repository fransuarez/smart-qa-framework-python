Feature: Fake Store API – Product CRUD

  Background:
    Given the API client is initialized

  Scenario: Authenticate and obtain JWT
    When I request a token with username "admin" and password "admin123"
    Then the response contains a field "token"

  Scenario Outline: Create a new product
    Given the payload for a new product is generated
    When I POST to "/products" with the payload
    Then the response matches the "Product" schema
    And the response contains a field "id"

    Examples:
      | title        | price |
      | "Widget A"   | 12.99 |
      | "Gadget B"   | 45.00 |