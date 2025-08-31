from pytest_bdd import scenarios, given, parsers
from src.models.scenario_context import ScenarioContext
from .common_steps import *

scenarios("../features/payment_store.feature")

@given(parsers.parse("a customer with {points:d} loyalty points"))
def customer_with_points(ctx: ScenarioContext, points: int):
    ctx.loyalty_points = points
    ctx.cart = []
