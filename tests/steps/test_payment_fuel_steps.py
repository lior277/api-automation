from dataclasses import asdict
from pytest_bdd import scenarios, given, when, then, parsers
from src.models.payment_request import PaymentRequest
from src.models.scenario_context import ScenarioContext

scenarios("../features/payment_fuel.feature")

@given("a registered customer with a valid credit card")
def customer_card(ctx: ScenarioContext):
    ctx.method = "CARD"

@when(parsers.parse("the customer requests to purchase {liters:d} liters of fuel at pump {pump:d}"))
def select_fuel(ctx: ScenarioContext, liters: int, pump: int):
    ctx.pump = pump
    # if you need multiple purchases, switch to += to accumulate
    ctx.liters = liters
    ctx.amount = float(liters * 6)

@when(parsers.parse("the payment API is called with amount {amount:f} ILS"))
def call_payment(ctx: ScenarioContext, amount: float, payment_api):
    session_id = ctx.session_id or f"pump-{ctx.pump}"
    req = PaymentRequest(
        session_id=session_id,
        amount=amount,
        method=ctx.method,
        currency="ILS",
    )
    resp = payment_api.charge_payment(asdict(req))
    ctx.payment_response = resp.json()

@then(parsers.parse('the payment response should be "{status}"'))
def verify_payment_status(ctx: ScenarioContext, status: str):
    assert ctx.payment_response and ctx.payment_response["status"] == status

@then("the transaction should be saved in the payment history")
def verify_saved(ctx: ScenarioContext):
    assert ctx.payment_response and "payment_id" in ctx.payment_response
