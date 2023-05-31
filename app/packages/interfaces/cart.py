from typing import Dict, Optional, List
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from packages.models import Addon, Product, Plan, Customer, Package, Order
from packages.strategies.cart_strategy import CartStrategy
from packages.strategies.producta_cart_strategy import ProductACartStrategy
from packages.strategies.productb_cart_strategy import ProductBCartStrategy
from packages.factories.payment_factory import PaymentFactory
from packages.factories.card_factory import CardFactory
from packages.factories.bank_factory import BankFactory
from packages.factories.store_factory import StoreFactory
from packages.factories.manual_factory import ManualFactory
from packages.exceptions import PaymentMethodException, PackageException
from packages.utils.hash import hash


class Cart():
    """Class to handle the shopping cart."""

    _product: Product
    _plan: Plan
    _customer: Customer
    _addon: QuerySet[Addon]

    def __init__(self, customer_id: Optional[int] = None, plan_id: Optional[int] = None, product_id: Optional[int] = None):

        if customer_id is not None:
            self.customer = customer_id

        if product_id is not None:
            self.product = product_id

        if plan_id is not None:
            self.plan = plan_id

    @property
    def product(self) -> Product:
        return self._product

    @product.setter
    def product(self, product_id) -> None:
        self._product = Product.objects.get(id=product_id)

    @property
    def plan(self) -> Plan:
        return self._plan

    @plan.setter
    def plan(self, plan_id) -> None:
        self._plan = Plan.objects.get(id=plan_id, product=self.product)

    @property
    def customer(self) -> Customer:
        return self._customer

    @customer.setter
    def customer(self, customer_id) -> None:
        self._customer = Customer.objects.get(id=customer_id)

    @property
    def addon(self) -> QuerySet[Addon]:
        return self._addon

    @addon.setter
    def addon(self, ids) -> None:
        self._addon = Addon.objects.filter(pk__in=ids)

    @property
    def package(self) -> Optional[Package]:
        try:
            return Package.objects.get(customer=self._customer, status="A", plan__product_id=self._product.pk)
        except ObjectDoesNotExist:
            return None

    def _get_cart_strategy(self, frequency: int, addons: List[Addon]) -> CartStrategy:
        """Get the cart strategy to use for order calculation"""

        if self.plan.product.code == "PRODUCT_A":
            return ProductACartStrategy(self.package, self.plan, self.addon, frequency, addons)
        elif self.plan.product.code == "PRODUCT_B":
            return ProductBCartStrategy(self.package, self.plan, self.addon, frequency, addons)
        else:
            raise

    def _get_payment_method_factory(self, method: str, order: Order) -> PaymentFactory | None:
        """Get payment method factory to use for payments."""

        if method == "CARD":
            return CardFactory(order)
        elif method == "BANK":
            return BankFactory(order)
        elif method == "STORE":
            return StoreFactory(order)
        elif method == "MANUAL":
            return ManualFactory(order)

        return None

    def get_plans(self):
        return Plan.objects.filter(product=self._product)

    def get_addons(self) -> QuerySet[Addon]:
        return Addon.objects.filter(plan=self._plan)

    def calculate_order(self, data: Dict[str, Dict]):
        """Create an order according to the plan/addons selected.

        Generate the hash of the order, including:
        - payment
        - subscription
        - start_date
        - end_date
        - package_data
        - customer
        """

        try:
            plan = Plan(**data["plan"])
            addons = [Addon(**addon) for addon in data["addon"]]
            frequency = int(str(data["frequency"]))
        except:
            raise ValueError(f"Unknown plan/addon")

        self.plan = plan.pk
        self.addon = [a.pk for a in addons]
        strategy = self._get_cart_strategy(frequency, addons)

        if strategy is None:
            raise ValueError(f"Unknown product for plan id: {plan.pk}")

        order = strategy.calculate_order()
        order.customer = self.customer
        order.product = self.product
        order.hash = hash(order)
        return order

    def execute_payment(self, method: str, order: Order):
        """Execute a payment according to the method and the order specified."""

        order_hash = order.hash
        order.hash = ''

        if hash(order) != order_hash:
            raise PackageException("Order has been altered")
        else:
            order.hash = order_hash
            no_orders = Package.objects.filter(order=order.hash).count()
            if no_orders > 0:
                raise PackageException("Order has been already processed")

        factory = self._get_payment_method_factory(method, order)

        if factory is None:
            raise PaymentMethodException(
                f"Unknown payment method type: {method}")
        else:
            factory.execute_payment()

    def confirm_payment(self, order_id: str):
        """Confirm payment received by service.

        Make Inactive the current package if there is one and make Active the package of the order_id."""

        package = Package.objects.filter(order=order_id).first()
        if package is not None:
            Package.objects.filter(
                status="A", plan__product_id=package.plan.product.pk).exclude(order=order_id).update(status="I")

            package.status = "A"
            package.save()
        else:
            raise PackageException("Order not found")
