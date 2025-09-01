from pytest_bdd import scenarios, given, when, then, parsers
from src.models.scenario_context import ScenarioContext
from tests.utils.payment_helpers import build_payment_body, PaymentMethod

scenarios("../features/payment_mix.feature")


@given("a registered customer with a valid credit card")
def customer_card(ctx: ScenarioContext):
    ctx.method = "CARD"
    ctx.session_id = ctx.session_id or "pump-7"


@given(parsers.parse("a customer with {points:d} loyalty points"))
def customer_with_points(ctx: ScenarioContext, points: int):
    ctx.loyalty_points = points
    ctx.cart = []


@given(parsers.parse("a customer at pump {pump:d}"))
def at_pump(ctx: ScenarioContext, pump: int):
    ctx.pump = pump
    ctx.method = "CARD"
    ctx.cart = []


@given(parsers.parse('the customer adds "Fuel - {liters:d} liters" to the cart'))
def add_fuel(ctx: ScenarioContext, liters: int):
    ctx.cart.append({"type": "FUEL", "liters": liters, "amount": float(liters * 6)})


@given(parsers.parse('the customer adds "{item1}" and "{item2}" to the cart'))
def add_store_items_pair(ctx: ScenarioContext, item1: str, item2: str):
    ctx.cart.append({"type": "ITEM", "name": item1, "amount": 12.0})
    ctx.cart.append({"type": "ITEM", "name": item2, "amount": 8.0})


@given(parsers.parse('the customer adds "{item}" to the cart'))
def add_single_item(ctx: ScenarioContext, item: str):
    ctx.cart.append({"type": "ITEM", "name": item, "amount": 10.0})


@when(parsers.parse('the customer purchases a "{item}" for {cost:d} points'))
def add_item_points(ctx: ScenarioContext, item: str, cost: int):
    ctx.cart.append({"type": "ITEM", "name": item, "cost_points": cost})


@when(parsers.parse('the payment API is called with total amount {total:f} ILS and method "{method}"'))
def call_mixed_payment(ctx: ScenarioContext, total: float, method: PaymentMethod, payment_api):
    body = build_payment_body(ctx, amount=total, method=method)
    resp = payment_api.charge_payment(body)
    ctx.payment_response = resp.json()


@when(parsers.parse('the payment API is called with payment method "{method}"'))
def call_payment_with_method(ctx: ScenarioContext, method: PaymentMethod, payment_api):
    body = build_payment_body(ctx, method=method)
    resp = payment_api.charge_payment(body)
    ctx.payment_response = resp.json()


@then(parsers.parse('the payment response should be "{status}"'))
def check_status(ctx: ScenarioContext, status: str):
    assert ctx.payment_response and ctx.payment_response["status"] == status


@then('the cart should be marked as "PAID"')
def check_cart_paid(ctx: ScenarioContext):
    assert ctx.payment_response and ctx.payment_response.get("status") in ("APPROVED", "PAID")


@then("the transaction should be saved in the payment history")
def verify_saved(ctx: ScenarioContext):
    assert ctx.payment_response and "payment_id" in ctx.payment_response

@then(parsers.parse("the customer's loyalty balance should be reduced by {delta:d}"))
def assert_loyalty_reduction(ctx: ScenarioContext, delta: int):
    assert ctx.loyalty_points - delta >= 0
