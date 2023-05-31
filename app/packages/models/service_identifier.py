from django.db import models
from packages.models import Customer, PaymentService


class ServiceIdentifier(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_service = models.ForeignKey(
        PaymentService, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=150)
