from django.db import models


class Charge(models.Model):
    """Model to manage all kind of charges performed."""

    type = models.CharField(max_length=50)
    response = models.JSONField()
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
