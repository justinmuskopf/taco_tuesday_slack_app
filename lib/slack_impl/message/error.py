from datetime import datetime

from lib.domain.domain_error import DomainError
from lib.slack.block.divider import Divider
from lib.slack.block.section import SectionBlock

import traceback

from lib.slack.block.text_block import TextBlock
from lib.slack.text.label import Label
from lib.slack.text.text import Text


class ErrorMessage:
    def __init__(self, e: Exception):
        self.ex = e
        self.blocks = []
        self.init()

    def _get_header(self):
        fields = [
            Text(text=f'*Reporter*: {self.ex.reporter if isinstance(self.ex, DomainError) else "Unknown"}', markdown_enabled=True).get_text(),
            Text(text=f'*Occurred At*: {datetime.now()}', markdown_enabled=True).get_text(),
            Text(text=f'*Cause*: {self.ex.__cause__ if self.ex.__cause__ else "Unknown"}', markdown_enabled=True).get_text(),
            Text(text=f'*Message*: {self.ex}', markdown_enabled=True).get_text()
        ]

        return SectionBlock(text='An error has occurred!', fields=fields)

    def init(self):
        self.blocks.append(Divider.get())
        self.blocks.append(TextBlock.get('*The following error has occurred:*', markdown_enabled=True))
        self.blocks.append(self._get_header().get_block())
        self.blocks.append(Divider.get())

        formatted_traceback = traceback.format_exc()[:2000]
        self.blocks.append(SectionBlock(text=f'```{formatted_traceback}```').get_block())

    def get_message(self):
        return self.blocks
