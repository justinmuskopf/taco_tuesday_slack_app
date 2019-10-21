from loguru import logger
from slack import WebClient

from lib.proc.handler.running_order import RunningOrderHandler
from lib.slack_impl.employee_ready_button import EmployeeReadyButton


class ActionHandler:
    def __init__(self, slack_client: WebClient):
        self.slack_client = slack_client

    @staticmethod
    def is_action_interaction(interaction):
        if 'type' not in interaction: return False

        return interaction['type'] == 'block_actions'

    @staticmethod
    def _is_button_action(action):
        return action['value'] == 'BUTTON'

    @staticmethod
    def _handle_button_action(slack_id, action):
        action_id = action['action_id']
        if not EmployeeReadyButton.is_ready_button_action(action_id):
            return

        logger.info(f'New Ready Button action for Slack ID #{slack_id}')
        EmployeeReadyButton.toggle_ready(slack_id)
        RunningOrderHandler.update_running_order_message()

    def handle(self, action: {}):
        actions = action['actions']
        slack_id = action['user']['id']
        for action in actions:
            logger.debug(f'Given Action: {action}')
            if self._is_button_action(action):
                self._handle_button_action(slack_id, action)

