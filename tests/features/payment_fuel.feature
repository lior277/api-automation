Feature: Fuel Payment at Gas Station

  Scenario: Successful fuel payment with credit card
    Given a registered customer with a valid credit card
    When the customer requests to purchase 40 liters of fuel at pump 7
    And the payment API is called with amount 240.00 ILS
    Then the payment response should be "APPROVED"
    And the transaction should be saved in the payment history
