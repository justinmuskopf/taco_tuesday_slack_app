from loguru import logger

from slack import WebClient

from lib.proc.channel_validator import ChannelValidator
from lib.proc.handler.base import BaseHandler
from lib.proc.handler.running_order import RunningOrderHandler
from lib.proc.view_parser import ViewParserSubmissionError
from lib.proc.handler.action import ActionHandler
from lib.proc.handler.view import ViewHandler


class InteractionHandler(BaseHandler):
    def __init__(self, slack_bot_token):
        slack_client = WebClient(slack_bot_token)
        super().__init__(slack_client)
        ChannelValidator(slack_client)

    @staticmethod
    def _handle_action(action: {}):
        logger.debug('Handling action...')
        ActionHandler.handle(action)

    @staticmethod
    def _handle_view(view: {}):
        logger.debug('Handling view...')
        ViewHandler.handle(view)

    @classmethod
    def handle_interaction(cls, interaction: {}):
        logger.debug('Handling Interaction!')
        try:
            if ActionHandler.is_action_interaction(interaction):
                cls._handle_action(interaction)
            elif ViewHandler.is_view_interaction(interaction):
                cls._handle_view(interaction)

            return ''
        except ViewParserSubmissionError as e:
            return e.block_error.get_block_error()

    @staticmethod
    def order(channel_id: str, trigger_id: str):
        if not RunningOrderHandler.OrderIsRunning:
            RunningOrderHandler.start_order(channel_id)

        ViewHandler.send_new_taco_order_modal(trigger_id)
