# src/api/payment_api.py

from requests import Response
from src.core.http import Http
from src.core.config import Config


class PaymentApi:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or Config.BASE_URL
        self.http = Http()

    def charge_payment(self, request_dto: object) -> Response:
        url = f"{self.base_url}/payments/charge"
        return self.http.execute_post_entry(url, request_dto)

    def refund_payment(self, request_dto: object) -> Response:
        url = f"{self.base_url}/payments/refund"
        return self.http.execute_post_entry(url, request_dto)

    def get_payment_status(self, payment_id: str) -> Response:
        url = f"{self.base_url}/payments/{payment_id}/status"
        return self.http.execute_get_entry(url)
