from lib.block.input_block import InputBlock
from lib.domain.label import Label
from lib.domain.taco import Taco


class TacoBlock(InputBlock):
    def __init__(self, taco: Taco):
        super().__init__(label=self._create_label(taco),
                         initial_value='0',
                         block_id=self.generate_block_id(taco),
                         action_id=self.generate_action_id(taco))
        self.taco = taco

    @staticmethod
    def _create_label(taco: Taco) -> Label:
        return Label('{} ({})'.format(taco.taco_type, taco.get_price_string())).get_label()

    @staticmethod
    def generate_block_id(taco: Taco) -> str:
        return f'{taco.taco_type}_blockId'

    @staticmethod
    def degenerate_block_id(block_id: str) -> str:
        return block_id.replace('_blockId', '')

    @staticmethod
    def generate_action_id(taco: Taco) -> str:
        return f'{taco.taco_type}_actionId'

    @staticmethod
    def degenerate_action_id(action_id: str) -> str:
        return action_id.replace('_actionId', '')

    @staticmethod
    def action_id_to_block_id(action_id: str) -> str:
        return action_id.replace('_actionId', '_blockId')

    @staticmethod
    def block_id_to_action_id(block_id: str) -> str:
        return block_id.replace('_blockId', '_actionId')
