from packages.interfaces.payment_method import PaymentMethod
from packages.exceptions import PaymentMethodException


class ManualMethod(PaymentMethod):
    """Class to handle manual payment methods."""

    def pay(self):
        self.create_package("MANUAL", "ACTIVE")
        self._payment_service.create_manual_charge()

    def subscribe(self):
        raise PaymentMethodException(
            "Manual payment method doesn't have subscribe option")
