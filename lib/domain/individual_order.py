from loguru import logger

from lib.domain.employee import Employee
from lib.domain.order import Order


class IndividualOrder(Order):
    ID = 0

    def __init__(self, employee: Employee):
        super().__init__()

        IndividualOrder.ID += 1
        self.internal_id = IndividualOrder.ID
        logger.debug(f'Creating individual order, internal_id = {self.internal_id}')

        self.employee = employee