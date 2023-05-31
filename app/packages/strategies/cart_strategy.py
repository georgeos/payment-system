from abc import ABC, abstractmethod
from dateutil.relativedelta import relativedelta
from typing import Optional, List
from datetime import date
from django.db.models import QuerySet
from packages.models import Package, Plan, Addon, Order
from packages.exceptions import PackageException
from packages.serializers.plan_package_serializer import PlanPackageSerializer
from packages.serializers.addon_package_serializer import AddonPackageSerializer
from packages.utils.converter import model_to_json


class CartStrategy(ABC):
    """Interface to handle different carts"""
    payment = None

    def __init__(self, package: Optional[Package], plan: Plan, addons: QuerySet[Addon], frequency: int, new_addons: List[Addon]):
        self.package = package
        self.plan = plan
        self.addons = addons
        self.frequency = frequency
        self.new_addons = new_addons

    @abstractmethod
    def calculate_order(self):
        """Calculate package for customer including one time payment, subscription,  dates."""

        self._calculate_total_subscription()
        self._calculate_dates()
        self._calculate_payment()
        return self._build_order()

    def _calculate_total_subscription(self):
        """Calculate the total subscription amount based on frequency."""

        self.total_subscription = self.plan.yearly_price if self.frequency == 12 else self.plan.monthly_price

        for a in self.addons:
            quantity = a.quantity
            if a.type == "VAR":
                quantity = next(
                    (na.quantity for na in self.new_addons if na.pk == a.pk), 0)
                a.quantity = quantity
                if quantity == 0:
                    raise PackageException(
                        f"Wrong quantity selected for addon {a.pk}")
            self.total_subscription += quantity * \
                (a.yearly_price if self.frequency == 12 else a.monthly_price)

    def _calculate_dates(self):

        self.start_date = date.today()
        self.end_date = self.start_date + self._calculate_date_delta()

    def _calculate_payment(self):
        """Calculate final payment (one time payment)."""

        if self.payment is None:
            self.payment = self.total_subscription
        else:
            self.payment = round(self.payment, 2)

    def _build_order(self) -> Order:
        """Return final package."""

        package_data = {}
        package_data["plan"] = model_to_json(PlanPackageSerializer, self.plan)
        package_data["addon"] = model_to_json(
            AddonPackageSerializer, self.addons)
        package_data["frequency"] = self.frequency

        return Order(
            payment=self.payment,
            subscription=self.total_subscription,
            start_date=self.start_date,
            end_date=self.end_date,
            package_data=package_data
        )

    def _calculate_date_delta(self) -> relativedelta:
        """Calculate the date delta based on frequency."""

        return relativedelta(years=1) if self.frequency == 12 else relativedelta(months=1)

    def _calculate_days_by_frequency(self) -> int:
        """Calculate the number of days for plan based on frequency."""

        return 365 if self.frequency == 12 else 30

    def _is_upgrade(self) -> bool:
        """Identify if the package is an upgrade for plan or addon"""
        assert self.package is not None

        if self.plan.quantity > self.package.plan.quantity:
            return True
        else:
            package_addons_ids = set(
                [a.pk for a in self.package.addon.all()])
            new_addons_ids = set([a.pk for a in self.addons])
            if len(package_addons_ids) >= len(new_addons_ids):
                return False
            else:
                return True
