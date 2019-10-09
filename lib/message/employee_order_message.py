from lib.button.button import Button
from lib.domain.individual_order import IndividualOrder
from lib.text.text import Text


class EmployeeOrderMessage:
    def __init__(self, user_id: str, order: IndividualOrder):
        self.user_id = user_id
        self.order = order

    def get_message(self) -> {}:
        return {
            'type': 'section',
            'text': Text('*Einsteins Do*\n4 Barbacoa, 3 Tripa, 4 Lengua, 2 Chicken Fajita - *$18.42*', markdown_enabled=True).get_text(),
            'accessory': Button('Ready', Button.PRIMARY).get_button()
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