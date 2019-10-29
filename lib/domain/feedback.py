import time
from pprint import pformat

from loguru import logger

from lib.domain.domain_error import DomainError
from lib.domain.employee import Employee


class ValidFeedbackTypes:
    FEEDBACK_TYPES = [
        'GENERAL',
        'SUGGESTION',
        'BUG'
    ]

    GENERAL = FEEDBACK_TYPES[0]
    SUGGESTION = FEEDBACK_TYPES[1]
    BUG = FEEDBACK_TYPES[2]

    @classmethod
    def is_valid(cls, feedback_type: str):
        return feedback_type in cls.FEEDBACK_TYPES


class FeedbackError(DomainError):
    def __init__(self, message: str):
        super().__init__(Feedback, message)


class Feedback:
    def __init__(self, employee: Employee, feedback_type: str, feedback: str):
        if not ValidFeedbackTypes.is_valid(feedback_type):
            raise FeedbackError(f'Invalid FeedbackType {feedback_type}, Valid: [{ValidFeedbackTypes.FEEDBACK_TYPES}]')

        self.created_at = time.time()
        self.employee = employee
        self.feedback_type = feedback_type
        self.feedback = feedback

        feedback_string = pformat(self.get_dict())
        if feedback_type == ValidFeedbackTypes.BUG:
            logger.warn(f'{feedback_type} submitted: {feedback_string}')
        else:
            logger.info(f'{feedback_type} submitted: {feedback_string}')

    def get_dict(self):
        return {
            'created_at': self.created_at,
            'employee': self.employee.get_dict(),
            'feedback_type': self.feedback_type,
            'feedback': self.feedback
        }
