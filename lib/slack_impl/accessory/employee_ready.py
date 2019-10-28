from lib.slack_impl.accessory.ready import ReadyButton


class EmployeeReadyButton(ReadyButton):
    ReadyEmployees = {}

    def __init__(self, slack_id: str, ready: bool = False):
        super().__init__(ready_text='Ready', not_ready_text='Not Ready', prefix=slack_id, ready=ready)
        self.slack_id = slack_id
        EmployeeReadyButton.ReadyEmployees[slack_id] = self.ready

    @classmethod
    def get(cls, slack_id: str) -> {}:
        if slack_id not in cls.ReadyEmployees: cls.ReadyEmployees[slack_id] = False

        return EmployeeReadyButton(slack_id, cls.ReadyEmployees[slack_id]).get_accessory()

    @classmethod
    def set_ready(cls, slack_id: str, ready: bool):
        cls.ReadyEmployees[slack_id] = ready

    @classmethod
    def toggle_ready(cls, slack_id: str):
        if slack_id not in cls.ReadyEmployees:
            cls.ReadyEmployees[slack_id] = False
        else:
            cls.ReadyEmployees[slack_id] = not cls.ReadyEmployees[slack_id]

    @staticmethod
    def get_slack_id_from_action_id(action_id: str):
        return action_id.split('_')[0]

    @classmethod
    def ready_button_belongs_to_slack_id(cls, action_id: str, slack_id: str):
        button_slack_id = cls.get_slack_id_from_action_id(action_id)
        return button_slack_id == slack_id

    def get_accessory(self) -> {}:
        self.ready = EmployeeReadyButton.ReadyEmployees[self.slack_id]

        return super().get_accessory()
