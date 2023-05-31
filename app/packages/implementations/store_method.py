from packages.interfaces.payment_method import PaymentMethod
from packages.exceptions import PaymentMethodException


class StoreMethod(PaymentMethod):
    """Class to handle store payment method."""

    def pay(self):
        self.create_package("STORE", "PENDING")
        payment_info = self.get_payment_info()
        self._payment_service.create_store_charge(*payment_info)

    def subscribe(self):
        raise PaymentMethodException(
            "Store payment method doesn't have subscribe option")
