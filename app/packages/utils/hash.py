import hmac
import hashlib
import base64
from django.db.models import Model
from django.forms.models import model_to_dict


def hash(data: Model):

    serialized = model_to_dict(data)
    string = str(serialized)

    dig = hmac.new(
        b"1234567890",
        string.encode("utf-8"),
        digestmod=hashlib.sha256).digest()
    encoded = base64.b64encode(dig).decode()
    return encoded
