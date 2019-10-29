from loguru import logger

from lib.domain.full_order import FullOrder
from lib.domain.individual_order import IndividualOrder
from lib.slack.block.divider import Divider
from lib.slack.message.employee_order_message import EmployeeOrderMessage
from lib.slack.text.text import Text
from lib.slack_impl.accessory.order_ready import OrderReadyButton


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

    def _get_header_section(self):
        return {
            'type': 'section',
            'text': Text.get(':taco: *Begin Order* :taco:', markdown_enabled=True)
        }

    def _get_running_order_section(self):
        return {
            'type': 'section',
            'text': Text.get(f'*Total*\n{self.order.get_full_order_string()}', markdown_enabled=True),
            'accessory': OrderReadyButton.get()
        }

    def get_message(self):
        # TODO: Only need to update the changed ones?
        running_order = self._get_running_order_section()

        pastor_price = self.order.get_individual_pastor_price()

        blocks = []
        blocks.append(Divider.get())
        blocks.append(self._get_header_section())
        blocks.append(Divider.get())
        blocks += [self.individual_messages[m].get_message(pastor_price) for m in self.individual_messages]
        blocks.append(Divider.get())
        blocks.append(running_order)
        blocks.append(Divider.get())

        logger.debug(blocks)

        return {
            'blocks': blocks
        }

    def get_blocks(self):
        return self.get_message()['blocks']
