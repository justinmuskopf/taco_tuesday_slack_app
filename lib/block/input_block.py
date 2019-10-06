from lib.block.block import Block
from lib.domain.label import Label


class InputBlock(Block):
    def __init__(self, label: Label, block_id: str = None, initial_value: str = '', action_id: str = None):
        super().__init__(block_type='input', block_id=block_id)
        self.initial_value = initial_value
        self.action_id = action_id
        self.label = label

    def get_block(self) -> {}:
        block = super().get_block()
        block['element'] = {
            'type': 'plain_text_input',
            'initial_value': self.initial_value

        }
        if self.action_id is not None:
            block['element']['action_id'] = self.action_id

        block['label'] = self.label

        return block
