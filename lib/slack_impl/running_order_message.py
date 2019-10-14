from lib.domain.employee import Employee
from lib.domain.full_order import FullOrder
from lib.domain.individual_order import IndividualOrder
from lib.slack.block.divider import Divider
from lib.slack.message.employee_order_message import EmployeeOrderMessage
from lib.slack.text.text import Text


class RunningOrderMessage:
    def __init__(self, order: FullOrder = None):
        self.order: FullOrder = FullOrder() if order is None else order
        self.individual_messages: {str, EmployeeOrderMessage} = {}

    @staticmethod
    def get():
        return RunningOrderMessage().get_message()

    def add_order(self, order: IndividualOrder, employee: Employee):
        slack_id = employee.slack_id
        if self.order.has_employee_order(slack_id):
            self.order.update_order(order)
        else:
            self.order.add_order(order)

        self.individual_messages[slack_id] = EmployeeOrderMessage(employee, order)

    def get_running_order_section(self):
        return {
            'type': 'section',
            'text': Text.get(str(self.order), markdown_enabled=True)
        }

    def get_message(self):
        # TODO: Only need to update the changed ones?
        running_order = self.get_running_order_section()

        blocks = [self.individual_messages[m] for m in self.individual_messages]
        blocks.append(Divider().get())
        blocks.append(running_order)

        return {
            'blocks': blocks
        }
