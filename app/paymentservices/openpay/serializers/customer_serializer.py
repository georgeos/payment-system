from rest_framework import serializers
from paymentservices.openpay.serializers.address_serializer import AddressSerializer


class CustomerSerializer(serializers.Serializer):

    id = serializers.CharField()
    external_id = serializers.CharField()
    name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    requires_account = serializers.BooleanField()
    phone_number = serializers.CharField()
    address = AddressSerializer()
    creation_date = serializers.DateTimeField()
