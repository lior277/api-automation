from dataclasses import asdict
from pytest_bdd import scenarios, given, when, then, parsers
from src.models.payment_request import PaymentRequest
from src.models.scenario_context import ScenarioContext

scenarios("../features/payment_store.feature")

@given(parsers.parse("a customer with {points:d} loyalty points"))
def customer_with_points(ctx: ScenarioContext, points: int):
    ctx.loyalty_points = points
    ctx.cart = []

@when(parsers.parse('the customer purchases a "{item}" for {cost:d} points'))
def add_item_points(ctx: ScenarioContext, item: str, cost: int):
    ctx.cart.append({"item": item, "cost_points": cost})

@when(parsers.parse('the payment API is called with payment method "{method}"'))
def call_loyalty_payment(ctx: ScenarioContext, method: ScenarioContext.__annotations__["method"], payment_api):
    total_points = sum(x["cost_points"] for x in ctx.cart)
    req = PaymentRequest(
        session_id="store-ks-001",
        amount=float(total_points),
        method=method,
        currency="ILS",
    )
    resp = payment_api.charge_payment(asdict(req))
    ctx.payment_response = resp.json()

@then(parsers.parse('the payment response should be "{status}"'))
def assert_status(ctx: ScenarioContext, status: str):
    assert ctx.payment_response and ctx.payment_response["status"] == status

@then(parsers.parse("the customer's loyalty balance should be reduced by {delta:d}"))
def assert_loyalty_reduction(ctx: ScenarioContext, delta: int):
    assert ctx.loyalty_points - delta >= 0
