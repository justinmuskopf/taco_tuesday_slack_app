from slack import WebClient
from loguru import logger
from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.domain.taco import Taco
from lib.proc.handler.running_order import RunningOrderHandler
from lib.slack_impl.taco_order_modal import TacoOrderModal
from lib.proc.view_parser import ViewParser


class ViewHandler:
    TACOS: [Taco] = TacoTuesdayApiHandler.get_tacos_from_api()

    def __init__(self, slack_client: WebClient):
        self.slack_client = slack_client
        self.view_parser = ViewParser()

    @staticmethod
    def is_view_interaction(interaction):
        if 'type' not in interaction: return False

        return interaction['type'] == 'view_submission'

    def handle_submission(self, view_submission: {}):
        order = self.view_parser.parse_submission_into_individual_order(view_submission)
        logger.debug(f'Received individual order: (SLACK_ID: {order.slack_id}): {order}')

        RunningOrderHandler.add_order(order)

    def handle(self, view: {}):
        logger.debug(f'View type: {view["type"]}')
        if view['type'] == 'view_submission': self.handle_submission(view)

    def send_new_taco_order_modal(self, trigger_id: str):
        # Show the ordering dialog to the user
        open_dialog = self.slack_client.views_open(trigger_id=trigger_id, view=TacoOrderModal().get_modal())
