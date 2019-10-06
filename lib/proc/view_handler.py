from slack import WebClient

from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.block.view_parser_error import ViewParserError
from lib.domain.taco import Taco
from lib.modal.taco_order_modal import TacoOrderModal
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
        print(order.tacos)



    def handle(self, view: {}):
        print(f'View type: {view["type"]}')
        if view['type'] == 'view_submission': self.handle_submission(view)

        #taco_order = TACO_ORDERS[user_id]

        # Update the message to show that we're in the process of taking their order
        # self.slack_client.chat_update(
        #     channel=TACO_ORDERS[user_id]["order_channel"],
        #     ts=taco_order["message_ts"],
        #     text=":white_check_mark: Order received!",
        # )

    def send_new_taco_order_modal(self, trigger_id: str):
        # Show the ordering dialog to the user
        print(self.TACOS)
        open_dialog = self.slack_client.views_open(trigger_id=trigger_id,
                                              view=TacoOrderModal().get_modal())


"""
        # Add the message_ts to the user's order info
        TACO_ORDERS[user_id]["message_ts"] = payload["message"]["ts"]

        print(f'Sending {user_id} a TacoOrder Modal...')

        # Show the ordering dialog to the user
        open_dialog = slack_client.views_open(trigger_id=payload["trigger_id"],
                                              view=get_taco_order_modal().get_modal())

        # Update the message to show that we're in the process of taking their order
        slack_client.chat_update(
            channel=TACO_ORDERS[user_id]["order_channel"],
            ts=payload["message"]["ts"],
            text=":pencil: Taking your order...",
        )

    

    return make_response("", 200)

"""