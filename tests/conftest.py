import re
import pytest
from src.api.payment_api import PaymentApi
from src.core.config import Config
from src.models.scenario_context import ScenarioContext

@pytest.fixture(scope="session")
def base_url():
    return Config.BASE_URL

@pytest.fixture(scope="session")
def payment_api():
    return PaymentApi(Config.BASE_URL)

@pytest.fixture
def ctx() -> ScenarioContext:
    return ScenarioContext()

@pytest.fixture(autouse=True)
def payments_api_mock(requests_mock, base_url):
    charge_url = f"{base_url}/payments/charge"
    refund_url = f"{base_url}/payments/refund"
    status_url_re = re.compile(rf"{re.escape(base_url)}/payments/.+/status")

    requests_mock.post(
        charge_url,
        json={"status": "APPROVED", "payment_id": "pay_123", "cart_status": "PAID"},
        status_code=200,
    )
    requests_mock.post(
        refund_url,
        json={"status": "REFUNDED"},
        status_code=200,
    )
    requests_mock.get(
        status_url_re,
        json={"status": "COMPLETED"},
        status_code=200,
    )

    return requests_mock
