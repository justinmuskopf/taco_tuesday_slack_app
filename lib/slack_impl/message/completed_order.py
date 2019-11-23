from config.order_config import TacoTuesdayOrderConfig
from lib.domain.full_order import FullOrder
from lib.slack.block.divider import Divider
from lib.slack.block.section import SectionBlock
from lib.slack.text.text import Text
from lib.slack_impl.message.running_order import RunningOrderMessage
from random import choice

class CompletedOrderMessage:
    TAQUERIA_NAME = TacoTuesdayOrderConfig().get_taqueria_name()
    TAQUERIA_ADDRESS = TacoTuesdayOrderConfig().get_taqueria_address()
    TAQUERIA_PHONE_NUMBER = TacoTuesdayOrderConfig().get_taqueria_phone_number()

    CALLEE_MESSAGES = [
        "<@{}> has been chosen to call!",
        "<@{}> has been deemed worthy to wield the telephone!",
        "<@{}> shall call.",
        "<@{}> call. Now.",
        "If <@{}> does not call *right now*, the world will explode!",
        "I'm really awkward on the phone... <@{}> will you call?",
        "There will be no tacos until <@{}> calls.",
        "<!here>, everyone shame <@{}> until they place the order!"
    ]

    def __init__(self, order: FullOrder):
        self.calling_employee = choice([slack_id for slack_id in order.individual_orders])
        self.running_message = RunningOrderMessage(order)

    @staticmethod
    def _get_header_section():
        return SectionBlock(text=':taco: *Completed Order* :taco:').get_block()

    def get_message(self):
        message = self.running_message.get_message()
        blocks = message['blocks']

        # TODO: This is a hotfix; make better
        blocks[1] = self._get_header_section()

        # Bye bye buttons!
        for block in blocks:
            if 'accessory' in block: block.pop('accessory')

        blocks.append(SectionBlock(text=f'*{self.TAQUERIA_NAME}*:').get_block())
        blocks.append(SectionBlock(text=f':earth_africa: {self.TAQUERIA_ADDRESS}').get_block())
        blocks.append(SectionBlock(text=f':phone: {self.TAQUERIA_PHONE_NUMBER}').get_block())
        blocks.append(SectionBlock(text=f':eyes: {choice(self.CALLEE_MESSAGES).format(self.calling_employee)}').get_block())

        blocks.append(Divider.get())

        return message

    def get_blocks(self):
        return self.get_message()['blocks']
