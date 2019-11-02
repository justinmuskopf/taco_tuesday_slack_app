import copy

from loguru import logger

from lib.domain.individual_order import IndividualOrder
from lib.domain.order import Order
from lib.domain.taco import ValidTacos


class FullOrder(Order):
    def __init__(self):
        super().__init__()

        self.individual_orders: {str: IndividualOrder} = {}

    def has_employee_order(self, slack_id: str):
        return slack_id in self.individual_orders

    def is_empty(self):
        logger.debug(f'Checking if I am empty... Individual Orders: {self.individual_orders}, len: {len(self.individual_orders)}')
        return len(self.individual_orders) == 0

    def add_order(self, order: IndividualOrder):
        [self.add(t, order[t])for t in order.tacos]

        self.individual_orders[order.slack_id] = order

    def remove_order(self, order: IndividualOrder):
        [self.remove(t, order[t]) for t in order.tacos]

        self.individual_orders.pop(order.slack_id)

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

    def get_individual_pastor_price(self) -> float:
        num_pastor = self.tacos['PASTOR']
        base_pastor_price = ValidTacos.get_taco_price('PASTOR').get()
        if num_pastor < 10:
            return base_pastor_price

        num_full_price = num_pastor % 10
        num_discounted = num_pastor - num_full_price

        total_pastor_price = (num_full_price * base_pastor_price) + num_discounted

        logger.debug(f'{num_full_price}, {num_discounted}, {total_pastor_price}, {num_pastor}')

        return float(total_pastor_price) / num_pastor

    def get_full_order_dict(self):
        pastor_price = self.get_individual_pastor_price()
        d = super().get_dict(pastor_price)
        d['individualOrders'] = [o.get_dict(pastor_price) for o in self.individual_orders.values()]

        return d

    def get_full_order_string(self):
        return self.get_order_string(self.get_individual_pastor_price())
