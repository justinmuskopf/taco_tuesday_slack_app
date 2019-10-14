from loguru import logger

from slack import WebClient

from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.proc.running_order_handler import RunningOrderHandler
from lib.proc.view_parser import ViewParserError
from lib.proc.action_handler import ActionHandler
from lib.proc.view_handler import ViewHandler


class InteractionHandler:
    def __init__(self, slack_bot_token):
        slack_client = WebClient(slack_bot_token)
        self.action_handler = ActionHandler(slack_client)
        self.view_handler = ViewHandler(slack_client)
        self.running_order_handler = RunningOrderHandler(slack_client)
        self.api_handler = TacoTuesdayApiHandler()

    def _handle_action(self, action: {}):
        logger.debug('Handling action...')
        self.action_handler.handle(action)

    def _handle_view(self, view: {}):
        logger.debug('Handling view...')
        self.view_handler.handle(view)

    def handle_interaction(self, interaction: {}):
        logger.debug('Handling Interaction!')
        try:
            if self.action_handler.is_action_interaction(interaction):
                self._handle_action(interaction)
            elif self.view_handler.is_view_interaction(interaction):
                self._handle_view(interaction)

            return ''
        except ViewParserError as e:
            return e.block_error.get_block_error()

    def order(self, channel_id: str, trigger_id: str):
        if RunningOrderHandler.OrderIsRunning:
            self.running_order_handler.update_running_order_message()
        else:
            self.running_order_handler.send_running_order_message(channel_id, trigger_id)

        self.view_handler.send_new_taco_order_modal(trigger_id)
