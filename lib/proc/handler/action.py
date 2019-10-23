from loguru import logger
from slack import WebClient

from lib.proc.handler.employee import EmployeeHandler
from lib.proc.handler.running_order import RunningOrderHandler
from lib.proc.handler.view import ViewHandler
from lib.slack_impl.accessory.employee_ready import EmployeeReadyButton
from lib.slack_impl.accessory.order_ready import OrderReadyButton
from lib.slack_impl.accessory.ready import ReadyButton


class ActionHandler:
    def __init__(self, slack_client: WebClient):
        self.slack_client = slack_client

    @staticmethod
    def _is_block_action(interaction: {}) -> bool:
        return 'type' in interaction and interaction['type'] == 'block_actions'

    @staticmethod
    def _is_message_action(interaction: {}) -> bool:
        return 'type' in interaction and interaction['type'] == 'message_action'

    @staticmethod
    def _is_button_action(action):
        return 'value' in action and action['value'] == 'BUTTON'

    @staticmethod
    def _is_feedback_action(action):
        return 'callback_id' in action and action['callback_id'] == 'FeedbackSubmissionCallback'

    @classmethod
    def is_action_interaction(cls, interaction):
        is_action = cls._is_block_action(interaction)
        is_action |= cls._is_message_action(interaction)

        return is_action

    @staticmethod
    def _handle_button_action(action_id, channel_id, slack_id, trigger_id):

        if not ReadyButton.is_ready_button_action(action_id): return

        if OrderReadyButton.is_order_button_action_id(action_id):
            if RunningOrderHandler.number_of_orders() == 0:
                EmployeeHandler.discipline_employee(slack_id,
                                                    channel_id,
                                                    'Really? What made you think that was an okay thing to do?')
                return
            if not OrderReadyButton.get_ready():
                return ViewHandler.send_order_submit_modal(trigger_id)
            else:
                return RunningOrderHandler.submit_order()

        if not EmployeeReadyButton.ready_button_belongs_to_slack_id(action_id, slack_id):
            EmployeeHandler.discipline_employee(slack_id,
                                                channel_id,
                                                "Didn't your mother ever tell you not to press someone else's buttons?")
            return
        else:
            logger.info(f'New Ready Button action for Slack ID #{slack_id}')
            EmployeeReadyButton.toggle_ready(slack_id)
            RunningOrderHandler.update_running_order_message()

    @classmethod
    def _handle_message_action(cls, action):
        trigger_id = action['trigger_id']
        if cls._is_feedback_action(action):
            return ViewHandler.send_feedback_modal(trigger_id)

    @classmethod
    def _handle_block_actions(cls, action_response):
        actions = action_response['actions']
        for action in actions:
            logger.debug(f'Given Action: {action}')
            if cls._is_button_action(action):
                logger.debug(f'Handling accessory action: {action}')
                slack_id = action_response['user']['id']
                trigger_id = action_response['trigger_id']
                channel_id = action_response['channel']['id']
                action_id = action['action_id']

                cls._handle_button_action(action_id, channel_id, slack_id, trigger_id)

    def handle(self, action: {}):
        if self._is_message_action(action):
            return self._handle_message_action(action)

        if self._is_block_action(action):
            return self._handle_block_actions(action)




