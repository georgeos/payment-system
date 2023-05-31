from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from packages.exceptions import PackageException
from packages.interfaces.cart import Cart
from packages.serializers.package_post_serializer import PackagePostSerializer
from packages.serializers.order_serializer import OrderSerializer


class OrderView(APIView):
    """View to handle order related requests."""

    def post(self, request, customer_id, product_id):
        serializer = PackagePostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                cart = Cart(customer_id=customer_id, product_id=product_id)
                order = cart.calculate_order(request.data)
                serialized = OrderSerializer(order)
                return Response(serialized.data, status=status.HTTP_200_OK)
            except PackageException as e:
                return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except ObjectDoesNotExist as e:
                return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
