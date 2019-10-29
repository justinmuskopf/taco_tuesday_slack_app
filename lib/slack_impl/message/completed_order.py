from lib.domain.full_order import FullOrder
from lib.slack.block.divider import Divider
from lib.slack.text.text import Text
from lib.slack_impl.message.running_order import RunningOrderMessage


class CompletedOrderMessage:
    def __init__(self, order: FullOrder):
        self.running_message = RunningOrderMessage(order)

    @staticmethod
    def _get_header_section():
        return {
            'type': 'section',
            'text': Text.get(':taco: *Completed Order* :taco:', markdown_enabled=True)
        }

    def get_message(self):
        message = self.running_message.get_message()
        blocks = message['blocks']

        # TODO: This is a hotfix; make better
        blocks[1] = self._get_header_section()

        # Bye bye buttons!
        for block in blocks:
            if 'accessory' in block: block.pop('accessory')

        blocks.append(Divider.get())

        return message

    def get_blocks(self):
        return self.get_message()['blocks']
