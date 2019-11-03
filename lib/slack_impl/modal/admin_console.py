from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.domain.employee import Employee
from lib.slack.block.divider import Divider
from lib.slack.block.section import SectionBlock
from lib.slack.modal.modal import Modal
from lib.slack_impl.accessory.admin import AdminButton
from lib.slack_impl.accessory.ready import ReadyButton


class AdminConsoleModal(Modal):
    CALLBACK_ID = 'AdminConsoleCallback'

    def __init__(self):
        super().__init__(title_text='Administrator Console', submit_text="LET'S DO IT!", callback_id=self.CALLBACK_ID)
        employees = TacoTuesdayApiHandler.get_all_employees()
        self.add_block(self._get_header())
        self.blocks += self._get_employees_section(employees)

    @classmethod
    def is_admin_console_submission(cls, callback_id: str):
        return callback_id.startswith(callback_id)

    @staticmethod
    def _get_header():
        return SectionBlock(text="ADMIN CONSOLE. **WARNING**: *_VERY BUGGY_*").get_block()

    @staticmethod
    def _get_employee_section(employee: Employee):
        return SectionBlock(
            text=employee.full_name,
            accessory=AdminButton(employee)
        )

    def _get_employees_section(self, employees: [Employee]):
        employee_sections = [self._get_employee_section(e).get_block() for e in employees]

        blocks = [SectionBlock(text="*KNOWN EMPLOYEES:*").get_block()]
        blocks += employee_sections
        blocks.append(Divider.get())

        return blocks
