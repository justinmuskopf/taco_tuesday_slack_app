from lib.slack.button.button import Button, ButtonStyle


class EmployeeReadyButton(Button):
    ReadyEmployees = {}

    def __init__(self, slack_id: str, ready=False):
        super().__init__(text='Not Ready' if not ready else 'Ready', style=ButtonStyle.DANGER if not ready else ButtonStyle.PRIMARY)
        self.slack_id = slack_id
        self.action_id = self._get_action_id(slack_id)

        EmployeeReadyButton.ReadyEmployees[slack_id] = ready

    @classmethod
    def get(cls, slack_id: str) -> {}:
        if slack_id not in cls.ReadyEmployees:
            cls.ReadyEmployees[slack_id] = False

        return EmployeeReadyButton(slack_id, cls.ReadyEmployees[slack_id]).get_button()

    @staticmethod
    def _get_action_id(slack_id: str) -> str:
        return f'{slack_id}_ReadyButton_actionId'

    @staticmethod
    def get_slack_id_from_action_id(action_id: str) -> str:
        return action_id.split('_')[0]

    @staticmethod
    def is_ready_button_action(action_id: str) -> bool:
        return '_ReadyButton_actionId' in action_id

    @classmethod
    def set_ready(cls, slack_id: str, ready: bool):
        cls.ReadyEmployees[slack_id] = ready

    @classmethod
    def toggle_ready(cls, slack_id: str):
        if slack_id not in cls.ReadyEmployees:
            cls.ReadyEmployees[slack_id] = False
        else:
            cls.ReadyEmployees[slack_id] = not cls.ReadyEmployees[slack_id]

    def get_button(self) -> {}:
        if self.ReadyEmployees[self.slack_id]:
            self.style = ButtonStyle.PRIMARY
            self.text = 'Ready'
        else:
            self.style = ButtonStyle.DANGER
            self.text = 'Not Ready'

        button = super().get_button()
        button['action_id'] = self.action_id

        return button
