from lib.domain.individual_order import IndividualOrder
from lib.slack.text.text import Text
from lib.slack_impl.accessory.employee_ready import EmployeeReadyButton


class EmployeeOrderMessage:
    def __init__(self, order: IndividualOrder):
        self.employee = order.employee
        self.order = order

    def _get_order_string(self) -> str:
        name = self.employee.name
        name_string = f'{name.nick_name}' if name.nick_name else str(name)

        return f'*{name_string}*\n{str(self.order)}'

    def get_message(self) -> {}:
        return {
            'type': 'section',
            'text': Text.get(self._get_order_string(), markdown_enabled=True),
            'accessory': EmployeeReadyButton.get(self.employee.slack_id)
        }
