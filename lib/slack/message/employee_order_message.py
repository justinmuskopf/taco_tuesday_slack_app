from lib.domain.individual_order import IndividualOrder
from lib.slack.text.text import Text
from lib.slack_impl.accessory.employee_ready import EmployeeReadyButton


class EmployeeOrderMessage:
    def __init__(self, order: IndividualOrder):
        self.employee = order.employee
        self.order = order

    def _get_order_string(self, pastor_price: float) -> str:
        name_string = f'{self.employee.nick_name}' if self.employee.nick_name else self.employee.full_name

        return f'*{name_string}*\n{self.order.get_order_string(pastor_price)}'

    def get_message(self, pastor_price: float) -> {}:
        return {
            'type': 'section',
            'text': Text.get(self._get_order_string(pastor_price), markdown_enabled=True),
            'accessory': EmployeeReadyButton.get(self.employee.slack_id)
        }
