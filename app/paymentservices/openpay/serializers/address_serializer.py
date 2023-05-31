from rest_framework import serializers


class AddressSerializer(serializers.Serializer):

    line1 = serializers.CharField()
    line2 = serializers.CharField()
    line3 = serializers.CharField()
    postal_code = serializers.CharField()
    state = serializers.CharField()
    city = serializers.CharField()
    country_code = serializers.CharField()
