from lib.domain.full_order import FullOrder
from lib.domain.individual_order import IndividualOrder
from lib.slack.block.divider import Divider
from lib.slack.message.employee_order_message import EmployeeOrderMessage
from lib.slack.text.text import Text


class RunningOrderMessage:
    def __init__(self, order: FullOrder = None):
        self.order: FullOrder = FullOrder()
        self.individual_messages: {str: EmployeeOrderMessage} = {}
        if order: self.ingest_full_order(order)

    def ingest_full_order(self, full_order: FullOrder):
        for order in full_order.get_orders():
            self.add_order(order)

    def add_order(self, order: IndividualOrder):
        if self.order.has_employee_order(order.slack_id):
            self.order.update_order(order)
        else:
            self.order.add_order(order)

        self.individual_messages[order.slack_id] = EmployeeOrderMessage(order)

    def _get_running_order_section(self):
        return {
            'type': 'section',
            'text': Text.get(f'*Total*\n{self.order}', markdown_enabled=True),
            'accessory': EmployeeReadyButton.get(self.employee.slack_id)
        }

    def get_message(self):
        # TODO: Only need to update the changed ones?
        running_order = self._get_running_order_section()

        blocks = [self.individual_messages[m].get_message() for m in self.individual_messages]
        blocks.append(Divider().get())
        blocks.append(running_order)

        return {
            'blocks': blocks
        }

    def get_blocks(self):
        return self.get_message()['blocks']
