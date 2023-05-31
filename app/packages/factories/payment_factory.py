from abc import ABC, abstractmethod
from django.conf import settings
from packages.interfaces.payment_method import PaymentMethod
from packages.implementations.card_method import CardMethod
from packages.models import Order, ServiceIdentifier, PaymentService as PaymentServiceModel
from paymentservices.interfaces.payment_service import PaymentService
from paymentservices.openpay.openpay import OpenpayService
from paymentservices.openpay.adapters.customer_adapter import CustomerAdapter


class PaymentFactory(ABC):
    """Factory to create payment methods."""

    def __init__(self, order: Order):
        self._order: Order = order
        self._customer = order.customer

    def _get_service_identifier(self):
        service_identifier = ServiceIdentifier.objects.filter(
            customer=self._customer,
            payment_service__name=settings.PAYMENT_SERVICE
        ).first()
        if service_identifier is not None and service_identifier.identifier is not None:
            return service_identifier.identifier
        else:
            return None

    def _create_service_identifier(self, identifier: str):
        payment_service_model = PaymentServiceModel.objects.get(
            name=settings.PAYMENT_SERVICE)
        ServiceIdentifier.objects.create(
            customer=self._customer,
            payment_service=payment_service_model,
            identfier=identifier
        )

    @abstractmethod
    def create_payment_service(self) -> PaymentService:
        """Create a payment service.

        1. Depending of the service it gets the ServiceIdentifier model to create the customer adapter
        2. When PaymentService is initilized, it validates if the identifier exists, otherwise it create the customer in the payment service
        3. Validates if the ServiceIdentifier model doesn't exist and the customer was created, then
            Creates the ServiceIdentifier model
        """

        if settings.PAYMENT_SERVICE == 'OpenpayService':
            identifier = self._get_service_identifier()
            customer_adapted = CustomerAdapter(
                self._customer, identifier).customer
            payment_service: PaymentService = OpenpayService(customer_adapted)

            if identifier is None and payment_service.service_identifier is not None:
                self._create_service_identifier(
                    payment_service.service_identifier)
            return payment_service
        else:
            raise NotImplementedError("Payment service not implemented yet.")

    @abstractmethod
    def create_payment_method(self, payment_service: PaymentService, order: Order) -> PaymentMethod:
        """Create a payment method according to the payment service."""

    def execute_payment(self) -> None:
        """Executes a payment, including the one time payment and subscription.

        If payment != subscription, means that there was prorration and subscription must start at start_date.
        If payment == subscription, means that there wasn't prorration and subscription must start at end_date, after first period is completed.
        """
        payment_service = self.create_payment_service()
        payment_method = self.create_payment_method(
            payment_service, self._order)

        payment_method.pay()

        if isinstance(payment_method, CardMethod):
            payment_method.subscribe()
