from datetime import date
from paymentservices.interfaces.payment_service import PaymentService
from paymentservices.manual.models import Customer


class ManualService(PaymentService):

    def __init__(self, customer: Customer):
        self._customer = customer

    def _create_customer(self):
        pass

    def create_card_charge(self, amount: float, description: str, order_id: str):
        raise NotImplementedError(
            "Manual payment service doesn't make card payments")

    def create_bank_charge(self, amount: float, description: str, order_id: str):
        raise NotImplementedError(
            "Manual payment service doesn't make bank payments")

    def create_store_charge(self, amount: float, description: str, order_id: str):
        raise NotImplementedError(
            "Manual payment service doesn't make store payments")

    def create_subscription(self, amount: float, description: str, date: date, frequency: int, order_id: str):
        raise NotImplementedError(
            "Manual payment service doesn't allow subscriptions")

    def create_manual_charge(self):
        """Magic method to create a manual charge."""

        print("Manual charge done!")
