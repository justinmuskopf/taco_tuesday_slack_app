from lib.slack.block.block import Block
from lib.slack.text.label import Label


class Modal:
    def __init__(self, title_text: str, submit_text: str = 'Submit', close_text: str = 'Cancel'):
        self.title_text = title_text
        self.submit_text = submit_text
        self.close_text = close_text
        self.blocks = []

    @staticmethod
    def get(title_text: str, submit_text: str = 'Submit', close_text: str = 'Cancel'):
        return Modal(title_text, submit_text, close_text).get_modal()

    def get_modal(self) -> {}:
        return {
            'type': 'modal',
            'title': Label.get(self.title_text),
            'submit': Label.get(self.submit_text),
            'close': Label.get(self.close_text),
            'blocks': self.blocks
        }

    def add_block(self, block: Block):
        self.blocks.append(block)
