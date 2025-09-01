Feature: Combined Transaction - Fuel and Store
  As a customer at a gas station
  I want to pay for both fuel and store items together
  So that I only have one transaction at checkout

  Scenario: Pay for fuel and store products together
    Given a customer at pump 3
    And the customer adds "Fuel - 30 liters" to the cart
    And the customer adds "Sandwich" to the cart
    And the customer adds "Soft Drink" to the cart
    When the payment API is called with total amount 200.00 ILS and method "CARD"
    Then the payment response should be "APPROVED"
    And the cart should be marked as "PAID"
