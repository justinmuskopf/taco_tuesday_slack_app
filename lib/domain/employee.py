from loguru import logger

from lib.domain.domain_error import DomainError

class EmployeeError(DomainError):
    def __init__(self, message):
        super().__init__(Employee, message)


class EmployeeNoSlackIdError(EmployeeError):
    def __init__(self):
        super().__init__('Employees must have a slack ID!')


class Employee:
    def __init__(self, slack_id: str, full_name: str, nick_name: str = '', api_id: str = None):
        if not self.is_valid_slack_id(slack_id):
            raise EmployeeNoSlackIdError()

        logger.debug(f'Creating Employee: {full_name} (Nickname: {nick_name}), Slack ID #{slack_id}')

        self.api_id = api_id
        self.slack_id = slack_id
        self.full_name = full_name
        self.nick_name = nick_name

    def __str__(self):
        return f'Id #{self.slack_id}: {self.full_name}'

    @staticmethod
    def is_valid_slack_id(slack_id: str) -> bool:
        if slack_id is None: return False
        if type(slack_id) is not str: return False
        if slack_id is '': return False

        return True

    def get_dict(self):
        d = {
            'fullName': self.full_name,
            'slackId': self.slack_id
        }

        if self.api_id:
            d['id'] = self.api_id

        if self.nick_name:
            d['nickName'] = self.nick_name

        return d

    @staticmethod
    def from_dict(user_info):
        try:
            user_profile = user_info['user']['profile']
            full_name = user_profile['real_name']
            slack_id = user_info['user']['id']
            nick_name = user_profile['display_name']

            return Employee(slack_id=slack_id, full_name=full_name, nick_name=nick_name)
        except KeyError or AttributeError:
            raise EmployeeError(f'Provided malformed dict: {user_info}!')

    def get_employee(self):
        employee = {
            'slackId': self.slack_id,
            'fullName': self.full_name
        }

        if self.nick_name:
            employee['nickName'] = self.nick_name

        return employee
