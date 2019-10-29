from lib.slack.block.block import Block
from lib.slack.block.section import SectionBlock
from lib.slack.text.text import Text


class TextBlock(SectionBlock):
    def __init__(self, text: str, markdown_enabled: bool = True):
        super().__init__(text=text)

    @staticmethod
    def get(text: str, markdown_enabled: bool = True):
        return TextBlock(text, markdown_enabled).get_block()

