# tests/steps/test_payment_mix_steps.py
from pytest_bdd import scenarios, given, when, then, parsers
from src.models.scenario_context import ScenarioContext
from tests.utils.payment_helpers import build_payment_body, PaymentMethod  # PaymentMethod = Literal["CARD","WALLET","CASH","LOYALTY"]

scenarios("../features/payment_mix.feature")

@given(parsers.parse("a customer at pump {pump:d}"))
def at_pump(ctx: ScenarioContext, pump: int):
    ctx.pump = pump
    ctx.method = "CARD"
    ctx.cart = []

@given(parsers.parse('the customer adds "Fuel - {liters:d} liters" to the cart'))
def add_fuel(ctx: ScenarioContext, liters: int):
    ctx.cart.append({"type": "FUEL", "liters": liters, "amount": float(liters * 6)})

@given(parsers.parse('the customer adds "{item}" to the cart'))
def add_single_item(ctx: ScenarioContext, item: str):
    # simple fixed pricing for store items in tests
    price = 12.0 if item.lower() == "sandwich" else 8.0 if item.lower() == "soft drink" else 10.0
    ctx.cart.append({"type": "ITEM", "name": item, "amount": price})

@when(parsers.parse('the payment API is called with total amount {total:f} ILS and method "{method}"'))
def call_payment_with_total(ctx: ScenarioContext, total: float, method: PaymentMethod, payment_api):
    body = build_payment_body(ctx, amount=total, method=method)
    resp = payment_api.charge_payment(body)
    ctx.payment_response = resp.json()

@then(parsers.parse('the payment response should be "{status}"'))
def check_status(ctx: ScenarioContext, status: str):
    assert ctx.payment_response and ctx.payment_response["status"] == status

@then('the cart should be marked as "PAID"')
def check_cart_paid(ctx: ScenarioContext):
    assert ctx.payment_response and ctx.payment_response.get("status") in ("APPROVED", "PAID")
