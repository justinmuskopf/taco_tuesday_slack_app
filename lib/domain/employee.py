
class Employee:
    def __init__(self, slack_id: str, first_name: str, last_name: str, nick_name=''):
        self.slack_id = slack_id
        self.first_name = first_name
        self.last_name = last_name
        self.nick_name = nick_name

    