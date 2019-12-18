import traceback

from lib.domain.feedback import Feedback
from lib.slack.block.divider import Divider
from lib.slack.block.section import SectionBlock
from lib.slack.block.text_block import TextBlock
from lib.slack.text.text import Text
from datetime import datetime


class FeedbackMessage:
    def __init__(self, fb: Feedback, issue_url: str = None):
        self.fb = fb
        self.blocks = []
        self.issue_url = issue_url
        self.init()

    def _get_header(self):
        fields = [
            Text(text=f'*Reporter*: {self.fb.employee.full_name}, (Slack ID #{self.fb.employee.slack_id})', markdown_enabled=True).get_text(),
            Text(text=f'*Occurred At*: {datetime.now()}', markdown_enabled=True).get_text(),
            Text(text=f'*Feedback Type*: {self.fb.feedback_type}', markdown_enabled=True).get_text()
        ]

        return SectionBlock(text='*A user has submitted feedback!*', fields=fields)

    def init(self):
        self.blocks.append(Divider.get())
        self.blocks.append(self._get_header().get_block())
        self.blocks.append(Divider.get())
        self.blocks.append(SectionBlock(text=f'*Feedback*:\n```{self.fb.feedback}```').get_block())
        self.blocks.append(Divider.get())

        if self.issue_url is not None:
            self.blocks.append(TextBlock.get(f'*Github Issue:* {self.issue_url}', markdown_enabled=True))
            self.blocks.append(Divider.get())

    def get_message(self):
        return self.blocks
