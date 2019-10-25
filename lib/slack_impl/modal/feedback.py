from lib.domain.feedback import ValidFeedbackTypes
from lib.slack.block.divider import Divider
from lib.slack.block.input_block import InputBlock
from lib.slack.block.section import SectionBlock
from lib.slack.accessory.static_select import StaticSelectBlock
from lib.slack.modal.modal import Modal
from lib.slack.text.label import Label


class FeedbackModal(Modal):
    CALLBACK_ID = 'SubmitFeedbackCallback'

    def __init__(self):
        super().__init__('Provide Feedback', callback_id=self.CALLBACK_ID, submit_text='Submit Feedback')
        self.add_block(self._get_select_section_block())
        self.add_block(InputBlock(label=Label.get('Feedback'), multiline=True, hint='Say Something, Anything!').get_block())

    @staticmethod
    def _get_select_section_block():
        select_block = StaticSelectBlock()
        [select_block.add_option(o) for o in ValidFeedbackTypes.FEEDBACK_TYPES]

        return SectionBlock('Type of Feedback', select_block).get_block()

    @classmethod
    def is_feedback_submission(cls, callback_id: str):
        return callback_id == cls.CALLBACK_ID

