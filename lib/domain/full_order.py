from lib.domain.individual_order import IndividualOrder
from lib.domain.order import Order
from lib.domain.taco import Taco


class FullOrder(Order):
    def __init__(self):
        super().__init__()

        self.individual_orders: {IndividualOrder} = {}

    def has_employee_order(self, slack_id):
        return slack_id in self.individual_orders

    def add_order(self, order: IndividualOrder):
        self.individual_orders[order.slack_id] = order

    def remove_order(self, order: IndividualOrder):
        tacos = order.tacos

        self.tacos = [self.tacos[t] - tacos[t] for t in tacos]
        self.price -= order.price

        return tacos

    def update_order(self, order):
        if order.slack_id in self.individual_orders:
            self.remove_order(order)

        self.add_order(order)
