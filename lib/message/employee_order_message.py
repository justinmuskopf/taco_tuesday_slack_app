from lib.button.button import Button
from lib.button.employee_ready_button import EmployeeReadyButton
from lib.domain.employee import Employee
from lib.domain.individual_order import IndividualOrder
from lib.text.text import Text


class EmployeeOrderMessage:
    def __init__(self, user_id: str, order: IndividualOrder, employee: Employee):
        self.user_id = user_id
        self.order = order
        self.employee = employee

    def _get_order_string(self) -> str:
        return f'*{self.employee.name}*\n{str(self.order)}'

    def get_message(self) -> {}:
        return {
            'type': 'section',
            'text': Text(self._get_order_string(), markdown_enabled=True).get_text(),
            'accessory': EmployeeReadyButton(self.employee).get_button()
        }

    """
    {
			"type": "section",a
			"text": {
				"type": "mrkdwn",
				"text": ""
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"emoji": true,
					"text": "Ready"
                },
                "style": "primary",
				"value": "click_me_123"
			}
		},
    """