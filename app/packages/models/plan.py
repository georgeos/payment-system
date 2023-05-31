from django.db import models
from packages.models import Addon, Product


class Plan(models.Model):
    """Model to manage plans."""

    STATUSES = [
        ("A", "Activo"),
        ("I", "Inactivo"),
        ("E", "Eliminado")
    ]

    code = models.CharField(max_length=35)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_of_measure = models.CharField(max_length=50)
    monthly_price = models.FloatField()
    yearly_price = models.FloatField()
    status = models.CharField(max_length=1, choices=STATUSES, default="A")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    addons = models.ManyToManyField(Addon)
