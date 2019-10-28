from slack.web.classes.blocks import SectionBlock, DividerBlock
from datetime import datetime

from lib.domain.domain_error import DomainError


class ErrorMessage:
    def __init__(self, e: Exception):
        self.exception = e
        self.text = 'The following error has occurred:'
        self.blocks = []

        self.init()

    def init(self):
        fields = []
        if isinstance(self.exception, DomainError):
            fields.append(f'*Reporter*: {self.exception.reporter}')
        else:
            fields.append('*Reporter*: Unknown')

        fields.append(f'*Occurred At*: {datetime.now()}')
        fields.append(f'*Cause: {self.exception.__cause__}')

        self.blocks.append(SectionBlock(fields=fields))
        self.blocks.append(DividerBlock())

        formatted_traceback = '\n\t'.join(self.exception.__traceback__.split('\n'))
        self.blocks.append(SectionBlock(fields=[formatted_traceback]))
