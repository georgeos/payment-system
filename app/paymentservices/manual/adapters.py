from packages.models import Customer
from paymentservices.manual.models import Customer as ManualCustomer


class CustomerAdapter():

    def __init__(self, customer: Customer):

        self.customer = ManualCustomer(
            id=customer.pk,
            name=customer.first_name,
            last_name=customer.last_name
        )
