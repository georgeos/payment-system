from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from packages.interfaces.cart import Cart
from packages.serializers.package_serializer import PackageSerializer


class PackageView(APIView):
    """View to respond all packages related requests."""

    def get(self, request, customer_id, product_id):
        try:
            cart = Cart(customer_id=customer_id, product_id=product_id)
            package = cart.package
            if package is None:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                serializer = PackageSerializer(package)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
