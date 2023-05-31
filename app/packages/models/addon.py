from django.db import models


class Addon(models.Model):
    """Model to manage addons for plans."""

    TYPES = [
        ("VAR", "Variable"),
        ("FIX", "Fixed")
    ]

    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    display_name = models.CharField(max_length=150)
    included = models.BooleanField(default=False)
    type = models.CharField(max_length=25, choices=TYPES, default="FIX")
    quantity = models.IntegerField()
    unit_of_measure = models.CharField(max_length=50)
    monthly_price = models.FloatField()
    yearly_price = models.FloatField()
