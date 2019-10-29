import traceback

from lib.domain.feedback import Feedback
from lib.slack.block.divider import Divider
from lib.slack.block.section import SectionBlock
from lib.slack.block.text_block import TextBlock
from lib.slack.text.text import Text
from datetime import datetime


class FeedbackMessage:
    def __init__(self, fb: Feedback):
        self.fb = fb
        self.blocks = []
        self.init()

    def _get_header(self):
        fields = [
            Text(text=f'*Reporter*: {self.fb.employee.name}, (Slack ID #{self.fb.employee.slack_id})').get_text(),
            Text(text=f'*Occurred At*: {datetime.now()}', markdown_enabled=True).get_text(),
            Text(text=f'*Feedback Type*: {self.fb.feedback_type}', markdown_enabled=True).get_text()
        ]

        return SectionBlock(text='A user has submitted feedback!', fields=fields)

    def init(self):
        self.blocks.append(Divider.get())
        self.blocks.append(TextBlock.get('*The following feedback has been submitted:*', markdown_enabled=True))
        self.blocks.append(self._get_header().get_block())
        self.blocks.append(Divider.get())
        self.blocks.append(Text(text=f'*Feedback*:\n```{self.fb.feedback}```', markdown_enabled=True).get_text())

    def get_message(self):
        return self.blocks
