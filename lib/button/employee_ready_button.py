from lib.button.button import Button
from lib.domain.employee import Employee


class EmployeeReadyButton(Button):
    def __init__(self, employee: Employee):
        super().__init__(text='Ready', style=Button.PRIMARY)

    def _get_action_id(self) -> str:
        return '_actionId'

    def get_button(self) -> {}:
        button = super().get_button()
        button['action_id'] = self._get_action_id()

        return button
