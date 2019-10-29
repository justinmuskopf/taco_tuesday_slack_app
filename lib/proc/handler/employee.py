import asyncio
import copy
import time
import threading

from loguru import logger
from slack import WebClient
from asyncio import AbstractEventLoop

from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler, NoSuchEmployeeError
from lib.domain.domain_error import DomainError
from lib.domain.employee import Employee, EmployeeNameError
from lib.proc.handler.base import BaseHandler


class EmployeeTrackerError(DomainError):
    def __init__(self, message: str):
        super().__init__(EmployeeHandler, message)


class EmployeeAlreadyExistsError(EmployeeTrackerError):
    def __init__(self, slack_id: str):
        super().__init__(f'An employee with Slack ID {slack_id} already exists!')


class EmployeeHandler(BaseHandler):
    EMPLOYEES: {str: Employee} = {}
    DISCIPLINE_THRESHOLD = 10
    DISCIPLINEES: {str: float} = {}

    @classmethod
    def has_employee(cls, slack_id: str):
        return slack_id in cls.EMPLOYEES

    @classmethod
    def get_employee(cls, slack_id: str):
        logger.debug(f'Retrieving Employee by Slack ID: {slack_id}')
        if cls.has_employee(slack_id):
            return copy.deepcopy(cls.EMPLOYEES[slack_id])

        try:
            employee = TacoTuesdayApiHandler.get_employee_by_slack_id(slack_id)
            cls.EMPLOYEES[slack_id] = employee
            return employee
        except NoSuchEmployeeError:
            logger.warning(f'Could not retrieve employee (Slack ID #{slack_id}) from API!')

        employee = cls.create_employee(slack_id)

        return copy.deepcopy(employee)

    @classmethod
    def create_employee(cls, slack_id: str):
        try:
            user_info = cls.SlackClient.users_info(user=slack_id)
            assert user_info['ok']

            employee = Employee.from_dict(user_info)

            return TacoTuesdayApiHandler.create_employee(employee)
        except AssertionError or KeyError:
            logger.error(f'Invalid response received from Slack API: {user_info}!')

    @classmethod
    def _since_last_discipline(cls, slack_id: str) -> float:
        return time.time() - cls.DISCIPLINEES[slack_id]

    @classmethod
    def _has_been_disciplined(cls, slack_id: str) -> bool:
        return slack_id in cls.DISCIPLINEES

    @classmethod
    def _should_be_disciplined(cls, slack_id: str) -> bool:
        if not cls._has_been_disciplined(slack_id):
            return True

        if cls._since_last_discipline(slack_id) > cls.DISCIPLINE_THRESHOLD:
            return True

        return False

    @classmethod
    def _forgive_wrongdoer(cls, channel_id: str, ts):
        logger.debug('Forgiving wrongdoer!')
        try:
            logger.debug(f'Deleting discipline message: ({channel_id}, {ts})')
            response = cls.SlackClient.chat_delete(channel=channel_id, ts=ts)
            assert response['ok']
            logger.debug('Forgave wrongdoer!')
        except AssertionError:
            logger.warning(f'Failed to forgive wrongdoer (ts: {ts})!')
        except Exception as e:
            logger.error(f'An unknown error occurred when forgiving wrongdoer: {e}')

    @classmethod
    def _queue_discipline_for_forgiveness(cls, channel_id: str, ts, forgive_in: float):
        logger.debug(f'Forgiving wrongdoer in {forgive_in} seconds...')
        #asyncio.get_event_loop().create_task(cls._forgive_wrongdoer(channel_id, ts, forgive_in))
        #threading.Timer(forgive_in, lambda: cls._forgive_wrongdoer(channel_id, ts)).start()

    @classmethod
    def discipline_employee(cls, slack_id: str, channel_id: str, text: str):
        if not cls._should_be_disciplined(slack_id): return

        cls.DISCIPLINEES[slack_id] = time.time()
        response = cls.SlackClient.chat_postEphemeral(user=slack_id, channel=channel_id, text=text)
        assert response['ok']

        cls._queue_discipline_for_forgiveness(channel_id, response['message_ts'], cls.DISCIPLINE_THRESHOLD)
