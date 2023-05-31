from django.db.models import Model
from abc import ABC, abstractmethod
from datetime import date
from packages.models import Order, Package, PackageAddon, Addon
from packages.exceptions import PackageException
from paymentservices.interfaces.payment_service import PaymentService


class PaymentMethod(ABC):
    """Interface to manage all payment methods"""

    def __init__(self, payment_service: PaymentService, order: Order):
        self._payment_service = payment_service
        self._order = order

        plan, addons, frequency = self._order.get_package_data()
        self._plan = plan
        self._addon = addons
        self._frequency = frequency

    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def subscribe(self):
        pass

    def create_package(self, payment_method: str, status: str):
        """Make Inactive the current package if there is one and create the new one."""

        if status == "ACTIVE":
            Package.objects.filter(customer=self._order.customer,
                                   plan__product_id=self._order.product.pk).update(status="I")

        package = Package.objects.create(
            customer=self._order.customer,
            frequency=self._frequency,
            plan=self._plan,
            payment_method=payment_method,
            start_date=self._order.start_date,
            end_date=self._order.end_date,
            renewal_date=date.today(),
            status=status[0],
            order=self._order.hash
        )

        for a in self._addon:
            try:
                addon = Addon.objects.get(id=a["id"])
                PackageAddon.objects.create(
                    package=package, addon=addon, quantity=a["quantity"])
            except Model.DoesNotExist:
                PackageException("Addon doesn't exist")

    def get_payment_info(self):
        amount = self._order.payment
        order_id = self._order.hash
        description = f"{self._plan.name} - {self._plan.product.name}"
        return amount, description, order_id
