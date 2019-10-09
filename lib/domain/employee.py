from lib.domain.employee_name import EmployeeName
from lib.domain.individual_order import IndividualOrder


class Employee:
    def __init__(self, slack_id: str, first_name: str, last_name: str, nick_name=''):
        self.slack_id = slack_id
        self.name = EmployeeName(first_name=first_name, last_name=last_name, nick_name=nick_name)
        self.orders: [IndividualOrder] = []

    def add_order(self, order: IndividualOrder):
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
