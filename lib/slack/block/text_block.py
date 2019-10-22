from lib.slack.block.block import Block
from lib.slack.text.text import Text


class TextBlock(Block):
    def __init__(self, text: str, markdown_enabled: bool = True):
        super().__init__('section')
        self.text = text
        self.markdown_enabled = markdown_enabled

    @staticmethod
    def get(text: str, markdown_enabled: bool = True):
        return TextBlock(text, markdown_enabled).get_block()

    def get_block(self):
        block = super().get_block()
        block['text'] = Text.get(self.text, markdown_enabled=True)

        return block
