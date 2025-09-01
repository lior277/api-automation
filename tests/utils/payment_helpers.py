from dataclasses import asdict
from typing import Literal, Optional
from src.models.payment_request import PaymentRequest
from src.models.scenario_context import ScenarioContext

PaymentMethod = Literal["CARD", "WALLET", "CASH", "LOYALTY"]

def build_payment_body(
    ctx: ScenarioContext, *, amount: Optional[float] = None, method: Optional[PaymentMethod] = None
) -> dict:
    session_id = ctx.session_id or (f"pump-{ctx.pump}-cart" if ctx.cart else f"pump-{ctx.pump}")

    total = ctx.amount
    if ctx.cart:
        amounts = [line.get("amount", 0.0) for line in ctx.cart if "amount" in line]
        points = [line.get("cost_points", 0) for line in ctx.cart if "cost_points" in line]
        total += sum(amounts)
        total += float(sum(points))

    body = PaymentRequest(
        session_id=session_id,
        amount=amount if amount is not None else total,
        method=method if method is not None else ctx.method,
        currency="ILS",
        lines=ctx.cart or None,
    )
    return asdict(body)
