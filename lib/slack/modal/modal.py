from lib.slack.block.block import Block
from lib.slack.text.label import Label


class Modal:
    ID = 10000

    def __init__(self, title_text: str, callback_id: str, submit_text: str = 'Submit', close_text: str = 'Cancel'):
        self.title_text = title_text
        self.submit_text = submit_text
        self.close_text = close_text
        self.uuid = Modal.ID + 1
        self.callback_id = f'{callback_id}_{self.uuid}'
        self.blocks = []

        Modal.ID += 1

    @staticmethod
    def get(title_text: str, submit_text: str = 'Submit', close_text: str = 'Cancel'):
        return Modal(title_text, submit_text, close_text).get_modal()

    def get_modal(self) -> {}:
        return {
            'type': 'modal',
            'title': Label.get(self.title_text),
            'submit': Label.get(self.submit_text),
            'close': Label.get(self.close_text),
            'callback_id': self.callback_id,
            'blocks': self.blocks
        }

    def add_block(self, block: Block):
        self.blocks.append(block)
