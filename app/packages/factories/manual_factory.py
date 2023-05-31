from packages.factories.payment_factory import PaymentFactory
from packages.implementations.manual_method import ManualMethod
from packages.interfaces.payment_method import PaymentMethod
from packages.models import Order
from paymentservices.interfaces.payment_service import PaymentService
from paymentservices.manual.manual import ManualService
from paymentservices.manual.adapters import CustomerAdapter


class ManualFactory(PaymentFactory):
    """Factory to create a ManualMethod payment."""

    def create_payment_service(self) -> PaymentService:
        customer_adapted = CustomerAdapter(self._customer).customer
        return ManualService(customer_adapted)

    def create_payment_method(self, payment_service: PaymentService, order: Order) -> PaymentMethod:
        return ManualMethod(payment_service, order)
