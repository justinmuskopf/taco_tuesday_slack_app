from lib.block.taco_block import TacoBlock
from lib.domain.taco import Taco
from lib.modal.modal import Modal


class TacoOrderModal(Modal):
    def __init__(self, tacos: [Taco]):
        super().__init__('Taco Order')
        self.tacos = tacos
        self.blocks = self._init_blocks(tacos)

    @staticmethod
    def _init_blocks(tacos) -> [TacoBlock]:
        return [TacoBlock(tacos[taco]).get_block() for taco in tacos]
