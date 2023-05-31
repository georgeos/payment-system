from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from packages.interfaces.cart import Cart
from packages.serializers.plan_package_serializer import PlanPackageSerializer


class PlanView(APIView):
    """View to respond all plan related requests."""

    def get(self, request, product_id):
        cart = Cart(product_id=product_id)
        plans = cart.get_plans()
        serializer = PlanPackageSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
