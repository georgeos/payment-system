from abc import ABC, abstractmethod
from datetime import date


class PaymentService(ABC):

    @abstractmethod
    def _create_customer(self):
        """Create a customer in the payment service."""

    @abstractmethod
    def create_card_charge(self, amount: float, description: str, order_id: str):
        """Create a charge using card."""

    @abstractmethod
    def create_bank_charge(self, amount: float, description: str, order_id: str):
        """Create a charge using bank method."""

    @abstractmethod
    def create_store_charge(self, amount: float, description: str, order_id: str):
        """Create a charge using card."""

    @abstractmethod
    def create_subscription(self, amount: float, description: str, date: date, frequency: int, order_id: str):
        """Create a subscription using card."""

    @abstractmethod
    def create_manual_charge(self):
        """Create a manual charge. Its a magic method"""
