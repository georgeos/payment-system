from django.db import models


class PaymentService(models.Model):

    name = models.CharField(max_length=50)
