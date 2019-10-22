import copy

from lib.domain.individual_order import IndividualOrder
from lib.domain.order import Order


class FullOrder(Order):
    def __init__(self):
        super().__init__()

        self.individual_orders: {str: IndividualOrder} = {}

    def has_employee_order(self, slack_id: str):
        return slack_id in self.individual_orders

    def add_order(self, order: IndividualOrder):
        [self.add(t, order[t])for t in order.tacos]

        self.individual_orders[order.slack_id] = order

    def remove_order(self, order: IndividualOrder):
        [self.remove(t, order[t]) for t in order.tacos]

        self.individual_orders[order.slack_id] = None

    def remove_employee_order(self, slack_id: str):
        if not self.has_employee_order(slack_id): return
        order = self.individual_orders[slack_id]

        self.remove_order(order)

    def update_order(self, order: IndividualOrder):
        if self.has_employee_order(order.slack_id):
            self.remove_employee_order(order.slack_id)

        self.add_order(order)

    def get_orders(self) -> [IndividualOrder]:
        return copy.deepcopy(self.individual_orders).values()

    def get_dict(self):
        d = super().get_dict()
        d['individualOrders'] = [o.get_dict() for o in self.individual_orders.values()]

        return d
