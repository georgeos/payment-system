from rest_framework import serializers
from packages.models import Package
from packages.serializers.plan_package_serializer import PlanPackageSerializer
from packages.serializers.customer_serializer import CustomerSerializer
from packages.serializers.addon_serializer import AddonSerializer


class PackageSerializer(serializers.ModelSerializer):

    plan = PlanPackageSerializer()
    customer = CustomerSerializer()
    addon = AddonSerializer(many=True)

    class Meta:
        model = Package
        fields = '__all__'
