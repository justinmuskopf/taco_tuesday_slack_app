from lib.domain.employee import Employee
from lib.domain.individual_order import IndividualOrder
from lib.domain.order import Order
from lib.slack.message.employee_order_message import EmployeeOrderMessage


class RunningOrderMessage:
    def __init__(self):
        self.individual_orders: {IndividualOrder} = {}
        self.individual_messages: {EmployeeOrderMessage} = {}
        self.order: Order = Order()

    def add_order(self, order: IndividualOrder, employee: Employee):
        slack_id = employee.slack_id
        self.individual_orders[slack_id] = order
        self.individual_messages[slack_id] = EmployeeOrderMessage(slack_id, order)

    # TODO: I hate this entire method
    def get_running_order(self):
        running_order = {}
        price = 0
        for order in self.individual_orders:
            price += order.price

            for taco_type in order.tacos:
                if taco_type not in running_order:
                    running_order[taco_type] = self.individual_orders[taco_type]
                else:
                    running_order[taco_type] += self.individual_orders[taco_type]

        return running_order

    def get_running_order_section(self):
        running_order = self.get_running_order()


    # TODO: Only need to update the changed ones?
    def get_message(self):
        individual_messages = []
        for slack_id in self.individual_orders:
            individual_messages.append(self.individual_orders[slack_id].get_message())

        running_order = self.get_running_order()

        blocks = individual_messages.copy()
        blocks.append()

        return {
            'blocks': individual_messages.append(running_order)
        }