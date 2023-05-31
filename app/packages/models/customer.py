from django.db import models
from packages.models import PaymentService


class Customer(models.Model):
    """Model to manage customers."""

    email = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    fiscal_name = models.CharField(max_length=80)
    phone = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    residence = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    internal_number = models.CharField(max_length=20)
    external_number = models.CharField(max_length=20)
    payment_service_id = models.ManyToManyField(
        PaymentService, through="ServiceIdentifier")
