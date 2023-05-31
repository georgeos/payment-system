from typing import Type
import json
from rest_framework.serializers import ModelSerializer
from django.db.models import Model, QuerySet


def model_to_json(serializer: Type[ModelSerializer], model: Model | QuerySet, many: bool = False):

    serialized = None

    if isinstance(model, Model):
        serialized = serializer(model).data
    elif isinstance(model, QuerySet):
        serialized = serializer(model, many=True).data

    return json.dumps(serialized)
