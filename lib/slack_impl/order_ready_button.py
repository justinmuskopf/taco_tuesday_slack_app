from lib.slack_impl.employee_ready_button import EmployeeReadyButton
from lib.slack_impl.ready_button import ReadyButton


class OrderReadyButton(ReadyButton):
    def __init__(self):
        super().__init__(ready_text='Submit', not_ready_text='Submit', prefix='OrderSubmit')

    @staticmethod
    def get_ready():
        return all(EmployeeReadyButton.ReadyEmployees.values())

    def is_order_button_action_id(self, action_id: str):
        return action_id == self.action_id

    @staticmethod
    def get():
        return OrderReadyButton().get_button()

    def get_button(self):
        self.ready = self._get_ready()

        return super().get_button()
