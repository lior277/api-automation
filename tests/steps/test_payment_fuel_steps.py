# tests/steps/test_payment_fuel_steps.py
from pytest_bdd import scenarios, given, when, then, parsers
from src.models.scenario_context import ScenarioContext
from tests.utils.payment_helpers import build_payment_body, PaymentMethod

scenarios("../features/payment_fuel.feature")

@given("a registered customer with a valid credit card")
def customer_card(ctx: ScenarioContext):
    ctx.method = "CARD"

@when(parsers.parse("the customer requests to purchase {liters:d} liters of fuel at pump {pump:d}"))
def select_fuel(ctx: ScenarioContext, liters: int, pump: int):
    ctx.pump = pump
    ctx.liters += liters
    ctx.amount += float(liters * 6)

@when(parsers.parse("the payment API is called with amount {amount:f} ILS"))
def call_payment_with_amount(ctx: ScenarioContext, amount: float, payment_api):
    body = build_payment_body(ctx, amount=amount)
    resp = payment_api.charge_payment(body)
    ctx.payment_response = resp.json()

@then(parsers.parse('the payment response should be "{status}"'))
def verify_payment_status(ctx: ScenarioContext, status: str):
    assert ctx.payment_response and ctx.payment_response["status"] == status

@then("the transaction should be saved in the payment history")
def verify_saved(ctx: ScenarioContext):
    assert ctx.payment_response and "payment_id" in ctx.payment_response
