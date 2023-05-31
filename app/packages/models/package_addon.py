from django.db import models
from packages.models import Package, Addon


class PackageAddon(models.Model):
    """Model to handle addons for packages."""

    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE)
    quantity = models.IntegerField()
