from rest_framework import serializers
from packages.models import Addon


class AddonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Addon
        fields = '__all__'
