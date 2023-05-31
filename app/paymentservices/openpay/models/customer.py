from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from paymentservices.openpay.models.address import Address


@dataclass
class Customer():

    id: Optional[str]
    external_id: str
    name: str
    last_name: str
    email: str
    requires_account: bool
    phone_number: str
    address: Address
    creation_date: Optional[datetime]
