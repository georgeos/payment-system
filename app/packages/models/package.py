from django.db import models
from packages.models import Addon, Customer, Plan


class Package(models.Model):
    """Model to manage customer packages."""

    FREQUENCIES = [
        (1, "Monthly"),
        (12, "Yearly")
    ]

    METHODS = [
        ("CARD", "Card"),
        ("STORE", "Store"),
        ("BANK", "Bank"),
        ("MANUAL", "Manual")
    ]

    STATUSES = [
        ("A", "Active"),
        ("P", "Pending"),
        ("I", "Inactive"),
        ("C", "Cancelled")
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    frequency = models.IntegerField(default=1, choices=FREQUENCIES)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    addon = models.ManyToManyField(Addon, through="PackageAddon")
    payment_method = models.CharField(max_length=50, choices=METHODS)
    start_date = models.DateField()
    end_date = models.DateField()
    renewal_date = models.DateField(null=True)
    status = models.CharField(max_length=1, choices=STATUSES, default="A")
    order = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
