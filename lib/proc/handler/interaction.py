from loguru import logger

from slack import WebClient

from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.proc.handler.employee import EmployeeHandler
from lib.proc.handler.running_order import RunningOrderHandler
from lib.proc.view_parser import ViewParserSubmissionError
from lib.proc.handler.action import ActionHandler
from lib.proc.handler.view import ViewHandler


class InteractionHandler:
    def __init__(self, slack_bot_token):
        slack_client = WebClient(slack_bot_token)
        self.action_handler = ActionHandler(slack_client)
        self.view_handler = ViewHandler(slack_client)
        self.running_order_handler = RunningOrderHandler(slack_client)
        self.api_handler = TacoTuesdayApiHandler()
        self.employee_handler = EmployeeHandler(slack_client)

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
        except ViewParserSubmissionError as e:
            return e.block_error.get_block_error()

    def order(self, channel_id: str, trigger_id: str):
        if not self.running_order_handler.OrderIsRunning:
            self.running_order_handler.start_order(channel_id)

        self.view_handler.send_new_taco_order_modal(trigger_id)
