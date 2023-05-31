from packages.factories.payment_factory import PaymentFactory
from packages.implementations.store_method import StoreMethod
from packages.interfaces.payment_method import PaymentMethod
from packages.models import Customer, Order
from paymentservices.interfaces.payment_service import PaymentService


class StoreFactory(PaymentFactory):
    """Factory to create a BankMethod payment."""

    def create_payment_service(self) -> PaymentService:
        return super().create_payment_service()

    def create_payment_method(self, payment_service: PaymentService, order: Order) -> PaymentMethod:
        return StoreMethod(payment_service, order)
