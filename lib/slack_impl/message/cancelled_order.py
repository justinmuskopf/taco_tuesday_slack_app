from lib.slack.block.divider import Divider
from lib.slack.block.section import SectionBlock


class CancelledOrderMessage:
    def __init__(self):
        self.blocks = [
            Divider().get(),
            SectionBlock(text=':taco::gun: Order Cancelled.').get_block(),
            Divider().get()
        ]

    def get_blocks(self):
        return self.blocks
