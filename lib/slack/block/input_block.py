from lib.slack.block.block import Block
from lib.slack.text.label import Label
from lib.slack.text.text import Text


class InputBlock(Block):
    def __init__(self, label: Label, block_id: str = None, initial_value: str = '', hint: str = '', action_id: str = None, multiline: bool = False):
        super().__init__(block_type='input', block_id=block_id)
        self.initial_value = initial_value
        self.action_id = action_id
        self.label = label
        self.multiline = multiline
        self.hint = hint

    @staticmethod
    def get(label: Label, block_id: str = None, initial_value: str = '', action_id: str = None):
        return InputBlock(label, block_id, initial_value, action_id).get_block()

    def get_block(self) -> {}:
        block = super().get_block()
        block['element'] = {
            'type': 'plain_text_input',
            'initial_value': self.initial_value
        }

        if self.multiline:
            block['element']['multiline'] = True

        if self.action_id is not None:
            block['element']['action_id'] = self.action_id

        if self.hint:
            block['hint'] = Text.get(self.hint)

        block['label'] = self.label

        return block
