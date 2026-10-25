Feature: End‑to‑end hybrid flow – API + UI + AI

  Scenario: Generate product via LLM, create via API, verify UI checkout
    Given the LLM generates a product payload
    When I POST the payload to the API "/products"
    Then the API response validates against the "Product" schema
    When I launch the browser and login to SauceDemo
    And I add the newly created product (by title) to the cart
    And I complete the checkout
    Then the visual AI validation of the checkout page succeeds