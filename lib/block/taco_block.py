from lib.block.input_block import InputBlock
from lib.domain.label import Label
from lib.domain.taco import Taco


class TacoBlock(InputBlock):
    def __init__(self, taco: Taco):
        super().__init__(label=self._create_label(taco), initial_value='0')
        self.taco = taco

    @staticmethod
    def _create_label(taco) -> Label:
        return Label('{} ({})'.format(taco.taco_type, taco.get_price_string())).get_label()

