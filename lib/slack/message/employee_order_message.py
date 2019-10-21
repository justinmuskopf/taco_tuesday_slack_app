from loguru import logger

from lib.domain.employee import Employee
from lib.domain.individual_order import IndividualOrder
from lib.slack.text.text import Text
from lib.slack_impl.employee_ready_button import EmployeeReadyButton


class EmployeeOrderMessage:
    def __init__(self, order: IndividualOrder):
        self.employee = order.employee
        self.order = order

    def _get_order_string(self) -> str:
        logger.debug("Getting Employee Order string!")
        return f'*{self.employee.name}*\n{str(self.order)}'

    def get_message(self) -> {}:
        return {
            'type': 'section',
            'text': Text.get(self._get_order_string(), markdown_enabled=True),
            'accessory': EmployeeReadyButton.get(self.employee.slack_id)
        }
