from packages.strategies.cart_strategy import CartStrategy


class ProductBCartStrategy(CartStrategy):
    """Strategy for a Product B cart"""

    def calculate_order(self):
        return super().calculate_order()
