from packages.interfaces.payment_method import PaymentMethod
from packages.exceptions import PaymentMethodException


class BankMethod(PaymentMethod):
    """Class to handle bank payment method."""

    def pay(self):
        self.create_package("BANK", "PENDING")
        payment_info = self.get_payment_info()
        self._payment_service.create_bank_charge(*payment_info)

    def subscribe(self):
        raise PaymentMethodException(
            "Bank payment method doesn't have subscribe option")
