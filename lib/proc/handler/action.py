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
