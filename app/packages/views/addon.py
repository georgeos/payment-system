from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from packages.interfaces.cart import Cart
from packages.serializers.addon_serializer import AddonSerializer


class AddonView(APIView):
    """View to respond all addons related requests."""

    def get(self, request, product_id, plan_id):
        cart = Cart(product_id=product_id, plan_id=plan_id)
        addons = cart.get_addons()
        serializer = AddonSerializer(addons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
