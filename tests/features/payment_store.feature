Feature: Store Product Payment
  As a customer in a gas station convenience store
  I want to pay with loyalty points
  So that I can redeem products without cash or card

  Scenario: Successful store product payment with loyalty points
    Given a customer with 500 loyalty points
    When the customer purchases a "Coffee" for 50 points
    And the payment API is called with payment method "LOYALTY"
    Then the payment response should be "APPROVED"
    And the customer's loyalty balance should be reduced by 50
