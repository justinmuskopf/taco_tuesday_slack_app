from lib.slack.button.button import Button, ButtonStyle


class EmployeeReadyButton(Button):
    def __init__(self, slack_id: str):
        super().__init__(text='Ready', style=ButtonStyle.PRIMARY)
        self.slack_id = slack_id
        self.action_id = self._get_action_id(slack_id)

    @staticmethod
    def get(slack_id: str) -> {}:
        return EmployeeReadyButton(slack_id).get_button()

    @staticmethod
    def _get_action_id(slack_id: str) -> str:
        return f'{slack_id}_ReadyButton_actionId'

    def get_button(self) -> {}:
        button = super().get_button()
        button['action_id'] = self.action_id

        return button
