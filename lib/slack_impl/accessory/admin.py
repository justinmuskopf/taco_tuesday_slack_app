from lib.domain.employee import Employee
from lib.slack_impl.accessory.ready import ReadyButton


class AdminButton(ReadyButton):
    def __init__(self, employee: Employee):
        self.employee = employee
        super().__init__(ready_text='Admin',
                         not_ready_text='Sans Admin',
                         prefix=self._get_prefix(employee),
                         ready=employee.admin)

    @staticmethod
    def _get_prefix(employee: Employee) -> str:
        return f'{employee.slack_id}_admin'

    @staticmethod
    def _get_slack_id_from_action_id(action_id: str):
        return action_id.split('_')[0]
