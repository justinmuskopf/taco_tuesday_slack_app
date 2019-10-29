from loguru import logger

from lib.domain.employee import Employee
from lib.domain.order import Order
from lib.slack_impl.accessory.employee_ready import EmployeeReadyButton


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

    def get_dict(self, pastor_price: float):
        d = super().get_dict(pastor_price)
        d['employee'] = self.employee.get_dict()

        return d
