from rest_framework import serializers
from packages.models import Package
from packages.serializers.plan_package_serializer import PlanPackageSerializer
from packages.serializers.addon_package_serializer import AddonPackageSerializer


class PackagePostSerializer(serializers.ModelSerializer):

    plan = PlanPackageSerializer()
    addon = AddonPackageSerializer(many=True)

    class Meta:
        model = Package
        fields = ['plan', 'addon', 'frequency']
