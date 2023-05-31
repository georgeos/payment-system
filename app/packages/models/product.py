from django.db import models
from packages.models import MailConfig


class Product(models.Model):
    """Model to manage products."""

    code = models.CharField(max_length=25)
    name = models.CharField(max_length=100)
    mail_config = models.ForeignKey(MailConfig, on_delete=models.CASCADE)
