from lib.slack.accessory.button import Button, ButtonStyle


class ReadyButton(Button):
    def __init__(self, ready_text: str, not_ready_text: str, prefix: str, ready=False):
        super().__init__(text=ready_text if ready else not_ready_text,
                         style=ButtonStyle.PRIMARY if ready else ButtonStyle.DANGER)

        self.action_id = self._get_action_id(prefix)
        self.ready_text = ready_text
        self.not_ready_text = not_ready_text
        self.prefix = prefix
        self.ready = ready

    @staticmethod
    def _get_action_id(prefix: str) -> str:
        return f'{prefix}_ReadyButton_actionId'

    @staticmethod
    def get_prefix_from_action_id(action_id: str) -> str:
        return action_id.split('_')[0]

    @staticmethod
    def is_ready_button_action(action_id: str) -> bool:
        return '_ReadyButton_actionId' in action_id

    def get_accessory(self) -> {}:
        if self.ready:
            self.style = ButtonStyle.PRIMARY
            self.text = self.ready_text
        else:
            self.style = ButtonStyle.DANGER
            self.text = self.not_ready_text

        button = super().get_accessory()
        button['action_id'] = self.action_id

        return button
