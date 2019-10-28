from loguru import logger

from lib.domain.domain_error import DomainError

class EmployeeError(DomainError):
    def __init__(self, message):
        super().__init__(Employee, message)


class EmployeeNoSlackIdError(EmployeeError):
    def __init__(self):
        super().__init__('Employees must have a slack ID!')


class EmployeeNameError(EmployeeError):
    def __init__(self, first_name='', last_name=''):
        if first_name and last_name:
            error_message = f'Error in name: {first_name} {last_name}'
        elif first_name and not last_name:
            error_message = f'Error in first name: {first_name}'
        elif last_name and not first_name:
            error_message = f'Error in last name: {last_name}'
        else:
            error_message = f'No employee name provided!'

        super().__init__(error_message)


class EmployeeName:
    def __init__(self, first_name: str, last_name: str, nick_name=''):
        if first_name and last_name:
            self.first_name = first_name
            self.last_name = last_name
        else:
            raise EmployeeNameError(first_name, last_name)

        if nick_name:
            self.nick_name = nick_name

    def __str__(self):
        name_string = f'{self.first_name} {self.last_name}'

        return name_string

    def get_dict(self):
        d = {
            'firstName': self.first_name,
            'lastName': self.last_name,
        }

        if self.nick_name:
            d['nickName'] = self.nick_name

        return d


class Employee:
    def __init__(self, slack_id: str, first_name: str, last_name: str, nick_name: str = '', api_id: str = None):
        if not self.is_valid_slack_id(slack_id):
            raise EmployeeNoSlackIdError()

        logger.debug(f'Creating Employee: {first_name} {last_name} (Nickname: {nick_name}), Slack ID #{slack_id}')

        self.api_id = api_id
        self.slack_id = slack_id
        self.name = EmployeeName(first_name=first_name, last_name=last_name, nick_name=nick_name)

    def __str__(self):
        return f'Id #{self.slack_id}: {self.name}'

    @staticmethod
    def is_valid_slack_id(slack_id: str) -> bool:
        if slack_id is None: return False
        if type(slack_id) is not str: return False
        if slack_id is '': return False

        return True

    def get_dict(self):
        d = self.name.get_dict()
        d['slackId'] = self.slack_id

        if self.api_id:
            d['id'] = self.api_id

        return d

    @staticmethod
    def from_dict(user_info):
        try:
            user_profile = user_info['user']['profile']

            split_real_name = user_profile['real_name'].split(' ')
            if len(split_real_name) < 2:
                raise EmployeeNameError()

            slack_id = user_info['user']['id']
            first_name, last_name = split_real_name[0], ' '.join(split_real_name[1:])
            nick_name = user_profile['display_name']

            return Employee(slack_id=slack_id, first_name=first_name, last_name=last_name, nick_name=nick_name)
        except KeyError or AttributeError:
            raise EmployeeError(f'Provided malformed dict: {user_info}!')

    def get_employee(self):
        employee = {
            'slackId': self.slack_id,
            'firstName': self.name.first_name,
            'lastName': self.name.last_name
        }

        if self.name.nick_name:
            employee['nickName'] = self.name.nick_name

        return employee
