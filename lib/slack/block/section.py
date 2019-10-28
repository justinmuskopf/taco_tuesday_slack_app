from lib.slack.accessory.accessory import Accessory
from lib.slack.block.block import Block
from lib.slack.text.text import Text


class SectionBlock(Block):
    def __init__(self, text: str, accessory: Accessory = None):
        super().__init__('section')
        self.text = Text(text)
        self.accessory = accessory

    def get_block(self):
        block = super().get_block()
        block['text'] = self.text.get_text()

        if self.accessory is not None:
            block['accessory'] = self.accessory.get_accessory()

        return block