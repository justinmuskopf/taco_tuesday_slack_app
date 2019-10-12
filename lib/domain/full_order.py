from lib.domain.individual_order import IndividualOrder
from lib.domain.order import Order


class FullOrder(Order):
    def __init__(self):
        super().__init__()

        self.individual_orders: {IndividualOrder} = {}

    def add_order(self, order: IndividualOrder):
        self.individual_orders