import copy

from loguru import logger
from slack import WebClient

from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler, NoSuchEmployeeError
from lib.domain.domain_error import DomainError
from lib.domain.employee import Employee, EmployeeNameError


class EmployeeTrackerError(DomainError):
    def __init__(self, message: str):
        super().__init__(EmployeeHandler, message)


class EmployeeAlreadyExistsError(EmployeeTrackerError):
    def __init__(self, slack_id: str):
        super().__init__(f'An employee with Slack ID {slack_id} already exists!')


class EmployeeHandler:
    EMPLOYEES: {str: Employee} = {}
    SlackClient: WebClient = None

    def __init__(self, slack_client: WebClient):
        if EmployeeHandler.SlackClient is None:
            EmployeeHandler.SlackClient = slack_client

    @classmethod
    def has_employee(cls, slack_id: str):
        return slack_id in cls.EMPLOYEES

    @classmethod
    def get_employee(cls, slack_id: str):
        if cls.has_employee(slack_id):
            return copy.deepcopy(cls.EMPLOYEES[slack_id])

        try:
            employee = TacoTuesdayApiHandler.get_employee_by_slack_id(slack_id)
        except NoSuchEmployeeError:
            logger.warning(f'Could not retrieve employee (Slack ID #{slack_id}) from API!')
            employee = cls.create_employee(slack_id)

        cls.EMPLOYEES[slack_id] = employee

        return copy.deepcopy(employee)

    @classmethod
    def create_employee(cls, slack_id: str):
        try:
            user_info = cls.SlackClient.users_info(user=slack_id)
            assert user_info['ok']

            employee = Employee.from_dict(user_info)

            return TacoTuesdayApiHandler.create_employee(employee)
        except AssertionError or KeyError as e:
            logger.error(f'Invalid response received from Slack API: {user_info}!')
