from lib.slack.block.divider import Divider
from lib.slack.block.text_block import TextBlock
from lib.slack.modal.modal import Modal


class OrderCancelModal(Modal):
    CALLBACK_ID = 'OrderCancelCallback'

    def __init__(self):
        super().__init__('Cancel Your Order?', submit_text="I'm Sure", callback_id=self.CALLBACK_ID)
        self.add_block(Divider.get())
        self.add_block(TextBlock.get("Do you _really_ want to cancel your order?\nTacos are pretty tasty..."))

    @classmethod
    def is_order_cancel_submission(cls, callback_id: str):
        return callback_id == cls.CALLBACK_ID
