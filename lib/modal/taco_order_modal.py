from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.block.taco_block import TacoBlock
from lib.domain.taco import Taco
from lib.modal.modal import Modal


class TacoOrderModal(Modal):
    TACOS = TacoTuesdayApiHandler.get_tacos_from_api()

    def __init__(self):
        super().__init__('Taco Order')
        self.blocks = self._init_blocks(self.TACOS)

    @staticmethod
    def _init_blocks(tacos) -> [TacoBlock]:
        return [TacoBlock(taco, tacos[taco]).get_block() for taco in tacos.keys()]
