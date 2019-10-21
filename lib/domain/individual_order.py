from loguru import logger

from lib.domain.employee import Employee
from lib.domain.order import Order
from lib.slack_impl.employee_ready_button import EmployeeReadyButton


class IndividualOrder(Order):
    ID = 1000

    def __init__(self, employee: Employee):
        super().__init__()

        IndividualOrder.ID += 1
        self.internal_id = IndividualOrder.ID
        logger.debug(f'Creating individual order, internal_id = {self.internal_id}')

        self.employee = employee
        self.slack_id = employee.slack_id

        EmployeeReadyButton.set_ready(self.slack_id, False)
