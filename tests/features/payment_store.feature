Feature: Store Product Payment
  As a customer in a gas station convenience store
  I want to pay with different payment methods
  So that I can redeem products with cash, card, or loyalty points

  Scenario: Successful store product payment with loyalty points
    Given a customer with 500 loyalty points
    When the customer purchases a "Coffee" for 50 points
    And the payment API is called with payment method "LOYALTY"
    Then the payment response should be "APPROVED"
    And the customer's loyalty balance should be reduced by 50

  Scenario: Successful store product payment with credit card
    Given a registered customer with a valid credit card
    When the customer purchases a "Sandwich" for 20 ILS
    And the payment API is called with payment method "CARD"
    Then the payment response should be "APPROVED"
    And the transaction should be saved in the payment history