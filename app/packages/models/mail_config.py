from django.db import models


class MailConfig(models.Model):
    """Model to manage mail configurations."""

    mail_from = models.CharField(max_length=100)
    mail_cc = models.CharField(max_length=100)
    subject = models.CharField(max_length=150)
    message = models.CharField(max_length=250)
    website = models.CharField(max_length=100)
    image = models.CharField(max_length=250)
