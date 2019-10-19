from loguru import logger

from lib.domain.order import Order


class IndividualOrder(Order):
    ID = 0

    def __init__(self, slack_id: str):
        super().__init__()

        IndividualOrder.ID += 1
        self.internal_id = IndividualOrder.ID
        logger.debug(f'Creating individual order, internal_id = {self.internal_id}')

        self.slack_id = slack_id
