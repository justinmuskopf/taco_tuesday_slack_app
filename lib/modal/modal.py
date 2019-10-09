from lib.block.block import Block
from lib.text.label import Label


class Modal:
    def __init__(self, title_text: str, submit_text: str = 'Submit', close_text: str = 'Cancel'):
        self.title_text = title_text
        self.submit_text = submit_text
        self.close_text = close_text
        self.blocks = []

    def get_modal(self) -> {}:
        return {
            'type': 'modal',
            'title': Label(self.title_text).get_label(),
            'submit': Label(self.submit_text).get_label(),
            'close': Label(self.close_text).get_label(),
            'blocks': self.blocks
        }

    def add_block(self, block: Block):
        self.blocks.append(block)
