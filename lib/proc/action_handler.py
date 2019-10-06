from slack import WebClient


class ActionHandler:
    def __init__(self, slack_client: WebClient):
        self.slack_client = slack_client

    @staticmethod
    def is_action_interaction(interaction):
        if 'type' not in interaction: return False

        return interaction['type'] == 'block_actions'

    def handle(self, action: {}):
        pass

"""
        # Add the message_ts to the user's order info
        TACO_ORDERS[user_id]["message_ts"] = payload["message"]["ts"]

        logger.debug(f'Sending {user_id} a TacoOrder Modal...')

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