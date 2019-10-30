from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.domain.individual_order import IndividualOrder
from lib.domain.taco import ValidTacos
from lib.slack_impl.block.taco import TacoBlock
from lib.slack.modal.modal import Modal


class TacoOrderModal(Modal):
    CALLBACK_ID = 'TacoOrderModalCallback'

    def __init__(self, order: IndividualOrder = None):
        super().__init__('Taco Order', self.CALLBACK_ID)
        self.order = order
        self.blocks = self._init_blocks(ValidTacos.get_tacos())

    def _init_blocks(self, tacos) -> [TacoBlock]:
        if self.order is not None:
            return [TacoBlock(taco, tacos[taco], initial_value=self.order.get_tacos(taco)).get_block() for taco in tacos.keys()]
        else:
            return [TacoBlock(taco, tacos[taco]).get_block() for taco in tacos.keys()]

    @classmethod
    def is_taco_order_submission(cls, callback_id: str):
        return callback_id.startswith(cls.CALLBACK_ID)
