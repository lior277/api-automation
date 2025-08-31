from pytest_bdd import scenarios, when, parsers
from src.models.scenario_context import ScenarioContext
from .common_steps import *

scenarios("../features/payment_fuel.feature")

@when(parsers.parse("the customer requests to purchase {liters:d} liters of fuel at pump {pump:d}"))
def select_fuel(ctx: ScenarioContext, liters: int, pump: int):
    ctx.pump = pump
    ctx.liters += liters
    ctx.amount += float(liters * 6)
