from lib.slack.block.divider import Divider
from lib.slack.block.text_block import TextBlock
from lib.slack.modal.modal import Modal
from lib.slack.text.text import Text


class OrderSubmitModal(Modal):
    CALLBACK_ID = 'OrderSubmitCallback'

    def __init__(self):
        super().__init__('Submit Order?', self.CALLBACK_ID)
        self.add_block(Divider.get())
        self.add_block(TextBlock.get("Do you _really_ want to submit this order?\nIt doesn't look like everyone is ready..."))

    @classmethod
    def is_order_submit_submission(cls, callback_id: str):
        return callback_id.startswith(cls.CALLBACK_ID)
