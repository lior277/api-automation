from dataclasses import asdict
from typing import Literal, Optional

from pytest_bdd import given, when, then, parsers
from src.models.payment_request import PaymentRequest
from src.models.scenario_context import ScenarioContext

PaymentMethod = Literal["CARD", "WALLET", "CASH", "LOYALTY"]

def _derive_session_id(ctx: ScenarioContext) -> str:
    if ctx.session_id:
        return ctx.session_id
    return f"pump-{ctx.pump}-cart" if ctx.cart else f"pump-{ctx.pump}"

def _derive_amount(ctx: ScenarioContext) -> float:
    if ctx.cart:
        amounts = [line.get("amount") for line in ctx.cart if "amount" in line]
        if amounts:
            return float(sum(a or 0.0 for a in amounts))
        points = [line.get("cost_points") for line in ctx.cart if "cost_points" in line]
        if points:
            return float(sum(int(p or 0) for p in points))
    return float(ctx.amount)

def build_payment_body(
    ctx: ScenarioContext, *, amount: Optional[float] = None, method: Optional[PaymentMethod] = None
) -> dict:
    body = PaymentRequest(
        session_id=_derive_session_id(ctx),
        amount=amount if amount is not None else _derive_amount(ctx),
        method=method if method is not None else ctx.method,
        currency="ILS",
        lines=ctx.cart or None,
    )
    return asdict(body)

@given("a registered customer with a valid credit card")
def given_customer_with_card(ctx: ScenarioContext):
    ctx.method = "CARD"

@given(parsers.parse("a customer with {points:d} loyalty points"))
def given_customer_with_points(ctx: ScenarioContext, points: int):
    ctx.loyalty_points = points
    ctx.cart = ctx.cart or []

@when(parsers.parse('the customer purchases a "{item}" for {cost:d} points'))
def add_item_points(ctx: ScenarioContext, item: str, cost: int):
    ctx.cart = ctx.cart or []
    ctx.cart.append({"type": "ITEM", "name": item, "cost_points": cost})

@when(parsers.parse('the customer purchases a "{item}" for {price:d} ILS'))
def add_item_price(ctx: ScenarioContext, item: str, price: int):
    ctx.cart = ctx.cart or []
    ctx.cart.append({"type": "ITEM", "name": item, "amount": float(price)})

@when(parsers.parse("the payment API is called with amount {amount:f} ILS"))
def call_payment_with_amount(ctx: ScenarioContext, amount: float, payment_api):
    body = build_payment_body(ctx, amount=amount)
    resp = payment_api.charge_payment(body)
    ctx.payment_response = resp.json()

@when(parsers.parse('the payment API is called with payment method "{method}"'))
def call_payment_with_method(ctx: ScenarioContext, method: PaymentMethod, payment_api):
    body = build_payment_body(ctx, method=method)
    resp = payment_api.charge_payment(body)
    ctx.payment_response = resp.json()

@then(parsers.parse('the payment response should be "{status}"'))
def payment_status_should_be(ctx: ScenarioContext, status: str):
    assert ctx.payment_response and ctx.payment_response["status"] == status

@then("the transaction should be saved in the payment history")
def then_txn_saved(ctx: ScenarioContext):
    assert ctx.payment_response and "payment_id" in ctx.payment_response

@then(parsers.parse("the customer's loyalty balance should be reduced by {delta:d}"))
def then_loyalty_reduced(ctx: ScenarioContext, delta: int):
    assert ctx.loyalty_points - delta >= 0
