from lib.domain.domain_error import DomainError
from lib.domain.employee_name import EmployeeName
from lib.domain.individual_order import IndividualOrder


class EmployeeError(DomainError):
    pass
class EmployeeNoSlackIdError(EmployeeError):
    def __init__(self):
        super().__init__('Employees must have a slack ID!')


class Employee:
    def __init__(self, slack_id: str, first_name: str, last_name: str, nick_name=''):
        if not self.is_valid_slack_id(slack_id):
            raise EmployeeNoSlackIdError()

        self.slack_id = slack_id
        self.name = EmployeeName(first_name=first_name, last_name=last_name, nick_name=nick_name)
        self.orders: [IndividualOrder] = []

    @staticmethod
    def is_valid_slack_id(slack_id: str) -> bool:
        if type(slack_id) is not str: return False
        if slack_id is None: return False
        if slack_id is '': return False

        return True

    def add_order(self, order: IndividualOrder):
        order.employee = self
        self.orders.append(order)

    def get_employee(self):
        employee = {
            'slackId': self.slack_id,
            'firstName': self.name.first_name,
            'lastName': self.name.last_name
        }

        if self.name.nick_name:
            employee['nickName'] = self.name.nick_name

        return employee
