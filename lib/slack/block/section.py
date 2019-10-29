from lib.slack.accessory.accessory import Accessory
from lib.slack.block.block import Block
from lib.slack.text.text import Text


class SectionBlock(Block):
    def __init__(self, text: str, accessory: Accessory = None, fields = None):
        super().__init__('section')
        self.text = Text.get(text, markdown_enabled=True)
        self.accessory = accessory
        self.fields = fields

    def get_block(self):
        block = super().get_block()
        block['text'] = self.text

        if self.accessory is not None:
            block['accessory'] = self.accessory.get_accessory()

        if self.fields is not None:
            block['fields'] = self.fields

        return block