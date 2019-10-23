from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.slack_impl.block.taco import TacoBlock
from lib.slack.modal.modal import Modal


class TacoOrderModal(Modal):
    TACOS = TacoTuesdayApiHandler.get_tacos_from_api()
    CALLBACK_ID = 'TacoOrderModalCallback'

    def __init__(self):
        super().__init__('Taco Order', self.CALLBACK_ID)
        self.blocks = self._init_blocks(self.TACOS)

    @staticmethod
    def _init_blocks(tacos) -> [TacoBlock]:
        return [TacoBlock(taco, tacos[taco]).get_block() for taco in tacos.keys()]

    @classmethod
    def is_taco_order_submission(cls, callback_id: str):
        return callback_id == cls.CALLBACK_ID