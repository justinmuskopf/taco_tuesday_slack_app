import os

from config.slack_config import TacoTuesdaySlackConfig
from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.domain.domain_error import DomainError
from lib.domain.feedback import Feedback, ValidFeedbackTypes
from lib.proc.handler.base import BaseHandler
from lib.slack_impl.message.feedback import FeedbackMessage
from lib.slack_impl.modal.feedback import FeedbackModal

from datetime import datetime


class FeedbackHandlerError(DomainError):
    def __init__(self, message: str):
        super().__init__(FeedbackHandler, message)


class FeedbackHandler(BaseHandler):
    DEBUG_CHANNEL = TacoTuesdaySlackConfig().get_debug_channel()
    RUNNING_FEEDBACK_TYPES = {}

    @classmethod
    def handle(cls, feedback: Feedback):
        if feedback.feedback_type == ValidFeedbackTypes.BUG:
            issue_name = f'TTSlackApp: {datetime.now()}'
            issue_body = f"**Reporter:** {feedback.employee.full_name} ({feedback.employee.slack_id})\n\n"
            issue_body += f"**Summary:**\n```\n{feedback.feedback}\n```"

            issue_url = TacoTuesdayApiHandler.create_github_issue(issue_name, issue_body)

            cls.SlackClient.chat_postEphemeral(channel=feedback.channel, user=feedback.employee.slack_id,
                                               text=f"Thank you for your feedback! Keep up on its progress here: {issue_url}")

            msg = FeedbackMessage(feedback, issue_url)
        else:
            msg = FeedbackMessage(feedback)

        cls.SlackClient.chat_postMessage(channel=cls.DEBUG_CHANNEL,
                                         blocks=msg.blocks)

    @classmethod
    def register_modal(cls, modal: FeedbackModal):
        if modal.uuid in cls.RUNNING_FEEDBACK_TYPES:
            raise FeedbackHandlerError(f"Feedback Modal ID {modal.uuid} already exists!")

        cls.RUNNING_FEEDBACK_TYPES[modal] = ValidFeedbackTypes.GENERAL

    @classmethod
    def register_type_change(cls, action_id: str, new_type: str):
        uuid = FeedbackModal.get_modal_id_from_select_block_action_id(action_id)
        cls.RUNNING_FEEDBACK_TYPES[uuid] = new_type

    @classmethod
    def get_type(cls, uuid: str):
        if uuid not in cls.RUNNING_FEEDBACK_TYPES:
            raise FeedbackHandlerError(f"No such Feedback Modal has been registered: {uuid}")

        return cls.RUNNING_FEEDBACK_TYPES[uuid]
