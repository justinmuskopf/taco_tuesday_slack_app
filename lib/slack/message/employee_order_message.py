from lib.slack.button import EmployeeReadyButton
from lib.domain.employee import Employee
from lib.domain.individual_order import IndividualOrder
from lib.slack.text.text import Text


class EmployeeOrderMessage:
    def __init__(self, employee: Employee, order: IndividualOrder):
        self.employee = employee
        self.order = order

    def _get_order_string(self) -> str:
        return f'*{self.employee.name}*\n{str(self.order)}'

    def get_message(self) -> {}:
        return {
            'type': 'section',
            'text': Text(self._get_order_string(), markdown_enabled=True).get_text(),
            'accessory': EmployeeReadyButton(self.employee).get_button()
        }
