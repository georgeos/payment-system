import requests
from typing import Any
from datetime import date
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from paymentservices.interfaces.payment_service import PaymentService
from paymentservices.openpay.models.customer import Customer
from paymentservices.openpay.serializers.customer_serializer import CustomerSerializer
from paymentservices.openpay.exceptions import OpenpayException


class OpenpayService(PaymentService):

    MERCHANT = settings.OPENPAY_MERCHANT
    KEY = settings.OPENPAY_KEY
    URL = f"https://sandbox-api.openpay.mx/v1/{MERCHANT}"
    HEADERS = {"Content-type": "application/json"}

    def __init__(self, customer: Customer):
        """Initialize customer.

        If customer identifier doesn't exist, it create a customer in the payment service."""
        self._customer = customer

        if self._customer.id is None:
            self._create_customer()
        else:
            customers_url = f"{self.URL}/customers/{self._customer.id}"
            response = requests.get(
                url=customers_url,
                headers=self.HEADERS,
                auth=(self.KEY, '')
            )

            if response.status_code != 200:
                raise OpenpayException(response.json()["description"])

    @property
    def service_identifier(self):
        return self._customer.id

    def _create_customer(self):

        customers_url = f"{self.URL}/customers"
        body = CustomerSerializer(self._customer).data
        data = JSONRenderer().render(body)
        response = requests.post(
            url=customers_url,
            headers=self.HEADERS,
            data=data,
            auth=(self.KEY, '')
        )

        if response.status_code == 201:
            self._customer.id = response.json()["id"]
        else:
            raise OpenpayException(response.json()["description"])

    def _make_charge(self, method: str, amount: float, description: str, order_id: str):

        charge_url = f"{self.URL}/customers/{self._customer.id}/charges"
        data = f"""{{
            "method": "{method}",
            "amount": {amount},
            "description": "{description}",
            "order_id": "{order_id}"
        }}"""
        response = requests.post(
            url=charge_url,
            headers=self.HEADERS,
            data=data,
            auth=(self.KEY, '')
        )

        if response.status_code == 200:
            charge = response.json()
            self._send_email(charge)
            return charge
        else:
            raise OpenpayException(response.json()["description"])

    def _send_email(self, response: Any):
        # TODO: Send email using a queue system
        print(f"Sending mail {response}")

    def create_card_charge(self, amount: float, description: str, order_id: str):
        print(
            f"Card charge using Openpay {amount} for {description} to customer {self._customer.id}")

    def create_bank_charge(self, amount: float, description: str, order_id: str):
        return self._make_charge("bank_account", amount, description, order_id)

    def create_store_charge(self, amount: float, description: str, order_id: str):
        return self._make_charge("store", amount, description, order_id)

    def create_subscription(self, amount: float, description: str, date: date, frequency: int, order_id: str):
        print(
            f"Subscription using Openpay {amount} for {description} to customer {self._customer.id}")

    def create_manual_charge(self):
        pass
