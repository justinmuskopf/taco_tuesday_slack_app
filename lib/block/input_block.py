from lib.block.block import Block
from lib.domain.label import Label


class InputBlock(Block):
    def __init__(self, label: Label, initial_value: str = ''):
        super().__init__('input')
        self.initial_value = initial_value
        self.label = label

    def get_block(self) -> {}:
        block = super().get_block()
        block['element'] = {
            'type': 'plain_text_input',
            'initial_value': self.initial_value
        }
        block['label'] = self.label

        return block
