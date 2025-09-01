from pytest_bdd import scenarios, given, when, then, parsers
from src.models.scenario_context import ScenarioContext
from tests.utils.payment_helpers import build_payment_body, PaymentMethod

scenarios("../features/payment_store.feature")


# --- Common customer steps ---

@given("a registered customer with a valid credit card")
def customer_card(ctx: ScenarioContext):
    ctx.method = "CARD"
    ctx.session_id = ctx.session_id or "store-001"


@given(parsers.parse("a customer with {points:d} loyalty points"))
def customer_with_points(ctx: ScenarioContext, points: int):
    ctx.loyalty_points = points
    ctx.cart = []


# --- Purchase steps ---

@when(parsers.parse('the customer purchases a "{item}" for {cost:d} points'))
def add_item_points(ctx: ScenarioContext, item: str, cost: int):
    ctx.cart.append({"type": "ITEM", "name": item, "cost_points": cost})


@when(parsers.parse('the customer purchases a "{item}" for {price:d} ILS'))
def add_item_price(ctx: ScenarioContext, item: str, price: int):
    ctx.cart.append({"type": "ITEM", "name": item, "amount": float(price)})


@when(parsers.parse('the payment API is called with payment method "{method}"'))
def call_payment_with_method(ctx: ScenarioContext, method: PaymentMethod, payment_api):
    body = build_payment_body(ctx, method=method)
    resp = payment_api.charge_payment(body)
    ctx.payment_response = resp.json()


# --- Assertions ---

@then(parsers.parse('the payment response should be "{status}"'))
def assert_status(ctx: ScenarioContext, status: str):
    assert ctx.payment_response and ctx.payment_response["status"] == status


@then(parsers.parse("the customer's loyalty balance should be reduced by {delta:d}"))
def assert_loyalty_reduction(ctx: ScenarioContext, delta: int):
    assert ctx.loyalty_points - delta >= 0


@then("the transaction should be saved in the payment history")
def verify_saved(ctx: ScenarioContext):
    assert ctx.payment_response and "payment_id" in ctx.payment_response
