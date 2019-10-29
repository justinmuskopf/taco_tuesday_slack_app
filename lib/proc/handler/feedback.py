import os

from lib.domain.feedback import Feedback
from lib.proc.handler.base import BaseHandler
from lib.slack_impl.message.feedback import FeedbackMessage
from lib.slack_impl.modal.feedback import FeedbackModal


class FeedbackHandler(BaseHandler):
    DEBUG_CHANNEL = os.environ['SLACK_DEBUG_CHANNEL']
    RUNNING_FEEDBACK_TYPES = {}

    @classmethod
    def handle(cls, feedback: Feedback):
        msg = FeedbackMessage(feedback)

        cls.SlackClient.chat_postMessage(channel=cls.DEBUG_CHANNEL,
                                         blocks=msg.blocks)

    @classmethod
    def register_type_change(cls, action_id: str, new_type: str):
        uuid = FeedbackModal.get_modal_id_from_select_block_action_id(action_id)
        cls.RUNNING_FEEDBACK_TYPES[uuid] = new_type
