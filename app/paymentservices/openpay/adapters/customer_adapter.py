from packages.models import Customer, ServiceIdentifier
from paymentservices.openpay.models.customer import Customer as OpenpayCustomer
from paymentservices.openpay.models.address import Address


class CustomerAdapter():

    def __init__(self, customer: Customer, identifier: str | None):

        self.customer = OpenpayCustomer(
            id=identifier,
            external_id=customer.pk,
            name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email,
            requires_account=False,
            phone_number=customer.phone,
            address=Address(
                line1=customer.residence,
                line2=None,
                line3=None,
                postal_code=customer.postal_code,
                state=customer.state,
                city=customer.city,
                country_code=customer.country
            ),
            creation_date=None
        )
