from rest_framework import serializers
from packages.models import Addon


class AddonPackageSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Addon
        fields = '__all__'
