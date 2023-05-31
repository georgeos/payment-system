from datetime import date
from packages.strategies.cart_strategy import CartStrategy
from packages.exceptions import PackageException


class ProductACartStrategy(CartStrategy):
    """Strategy for a Product A cart"""

    def calculate_order(self):

        self._calculate_total_subscription()
        self._calculate_dates()

        if self.package is not None:
            if self._is_upgrade():
                self._calculate_one_time_payment()
            elif self.frequency > self.package.frequency:
                pass
            else:
                raise PackageException(
                    "Wrong plan selection: No upgrade / No greather frequency")

        self._calculate_payment()
        return self._build_order()

    def _calculate_dates(self) -> None:
        """Calculate stard/end date for package"""

        if self.package is None or date.today() > self.package.end_date:
            self.start_date = date.today()
            self.end_date = self.start_date + self._calculate_date_delta()
        else:
            self.start_date = self.package.end_date
            self.end_date = self.start_date + self._calculate_date_delta()
            self.renewal_date = date.today()

    def _calculate_one_time_payment(self):
        """Calculate one time payment for an extension.

        In case it is an upgrade, charges a one time payment for the prorration of the new plan."""
        assert self.package is not None

        date_diff = self.package.end_date - date.today()
        pending_days = abs(date_diff).days
        self.payment = (self.total_subscription * pending_days) / \
            self._calculate_days_by_frequency()
