from rest_framework import serializers
from packages.models import Plan


class PlanPackageSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Plan
        fields = ['id', 'code', 'name', 'display_name', 'quantity',
                  'unit_of_measure', 'monthly_price', 'yearly_price', 'status']
