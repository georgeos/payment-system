from packages.interfaces.payment_method import PaymentMethod


class CardMethod(PaymentMethod):
    """Class to handle credit/debit card payment method."""

    def pay(self):
        payment_info = self.get_payment_info()
        self._payment_service.create_card_charge(*payment_info)

    def subscribe(self):
        # self._payment_service.create_subscription(amount, description, date, frequency, order_id)
        pass
