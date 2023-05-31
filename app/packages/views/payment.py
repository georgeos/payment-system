from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from packages.models import Order
from packages.serializers.order_serializer import OrderSerializer
from packages.interfaces.cart import Cart
from packages.exceptions import PaymentMethodException, PackageException
from paymentservices.openpay.exceptions import OpenpayException


class PaymentView(APIView):
    """View to handle payment requests."""

    def post(self, request, customer_id: int, product_id: int):
        order_data = request.data["order"]
        method_data = request.data["method"]
        serialized = OrderSerializer(data=order_data)

        if serialized.is_valid(raise_exception=True):
            try:
                order = Order(**serialized.validated_data)  # type: ignore
                cart = Cart(customer_id=customer_id, product_id=product_id)
                with transaction.atomic():
                    cart.execute_payment(method_data, order)
            except OpenpayException as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except PackageException as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except PaymentMethodException as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except NotImplementedError as e:
                return Response({"error": str(e)}, status=status.HTTP_501_NOT_IMPLEMENTED)
        return Response(status=status.HTTP_200_OK)
