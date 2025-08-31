from dataclasses import asdict
from pytest_bdd import scenarios, given, when, then, parsers
from src.models.payment_request import PaymentRequest
from src.models.scenario_context import ScenarioContext

scenarios("../features/payment_mix.feature")

@given(parsers.parse("a customer at pump {pump:d}"))
def at_pump(ctx: ScenarioContext, pump: int):
    ctx.pump = pump
    ctx.method = "CARD"
    ctx.cart = []

@given(parsers.parse('the customer adds "Fuel - {liters:d} liters" to the cart'))
def add_fuel(ctx: ScenarioContext, liters: int):
    ctx.cart.append({"type": "FUEL", "liters": liters, "amount": float(liters * 6)})

# supports both "two-items" line...
@given(parsers.parse('the customer adds "{item1}" and "{item2}" to the cart'))
def add_store_items_pair(ctx: ScenarioContext, item1: str, item2: str):
    ctx.cart.append({"type": "ITEM", "name": item1, "amount": 12.0})
    ctx.cart.append({"type": "ITEM", "name": item2, "amount": 8.0})

# ...and single item per line
@given(parsers.parse('the customer adds "{item}" to the cart'))
def add_single_item(ctx: ScenarioContext, item: str):
    ctx.cart.append({"type": "ITEM", "name": item, "amount": 10.0})

@when(parsers.parse('the payment API is called with total amount {total:f} ILS and method "{method}"'))
def call_mixed_payment(ctx: ScenarioContext, total: float, method: ScenarioContext.__annotations__["method"], payment_api):
    # method param is type-compatible with Literal in ctx
    session_id = f"pump-{ctx.pump}-cart"
    req = PaymentRequest(
        session_id=session_id,
        amount=total,
        method=method,
        currency="ILS",
        lines=ctx.cart,
    )
    resp = payment_api.charge_payment(asdict(req))
    ctx.payment_response = resp.json()

@then(parsers.parse('the payment response should be "{status}"'))
def check_status(ctx: ScenarioContext, status: str):
    assert ctx.payment_response and ctx.payment_response["status"] == status

@then('the cart should be marked as "PAID"')
def check_cart_paid(ctx: ScenarioContext):
    assert ctx.payment_response and ctx.payment_response.get("status") in ("APPROVED", "PAID")
