from pytest_bdd import scenarios, given, parsers
from src.models.scenario_context import ScenarioContext
from .common_steps import *

scenarios("../features/payment_mix.feature")

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
