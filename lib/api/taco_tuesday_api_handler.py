from http import HTTPStatus
from json import JSONDecodeError

from lib.domain.domain_error import DomainError
from lib.domain.employee import Employee
from lib.domain.full_order import FullOrder
from lib.domain.taco import Taco, ValidTacos
from loguru import logger
import copy
import os
import requests
import json


class TacoTuesdayApiError(DomainError):
    def __init__(self, message: str):
        super().__init__(TacoTuesdayApiHandler, message)


class NoSuchEmployeeError(TacoTuesdayApiError):
    def __init__(self, slack_id: str):
        super().__init__(f'Could not find Employee with Slack ID: {slack_id}!')


class TacoTuesdayApiHandler:
    API_BASE_URL = os.environ['TT_BASE_API_URL']
    API_KEY = os.environ['TT_API_KEY']

    TACOS = {}

    # HTTP Methods
    GET = requests.get
    POST = requests.post
    PATCH = requests.patch
    DELETE = requests.delete

    def __init__(self):
        self.get_tacos_from_api()

    @classmethod
    def form_api_url(cls, extension):
        return f'{cls.API_BASE_URL}/{extension}'

    @classmethod
    def get_json_from_response(cls, response):
        try:
            return response.json()
        except JSONDecodeError:
            return None

    @classmethod
    def do_api_interaction(cls, request_method, uri: str, headers={}, params={}, body_object={}):
        logger.debug(f'Performing HTTP Method {request_method} --> {uri} (params = {params}) (body = {body_object})')

        api_url = cls.form_api_url(uri)

        try:
            response = request_method(api_url, headers=headers, params=params, json=body_object)
            assert response.content is not None

            logger.debug(f'Returned from API: {response.content}')

            return response
        except Exception as e:
            raise TacoTuesdayApiError(str(e))

    # TODO: Email when can't get Tacos
    @classmethod
    def get_tacos_from_api(cls):
        if cls.TACOS:
            return cls.TACOS

        logger.debug('Initializing Tacos!')

        tacos = cls.do_api_interaction(cls.GET, '/tacos').json()

        # TODO: catch JSON error
        for taco in tacos:
            logger.info(f'Loading taco: {taco}')
            taco_type = taco['type']
            cls.TACOS[taco_type] = Taco(taco_type=taco_type, price=taco['price'])

        ValidTacos.set_tacos(copy.deepcopy(cls.TACOS))

        return cls.TACOS

    @classmethod
    def force_taco_refresh(cls):
        logger.warn('Forcing Taco refresh...')
        cls.TACOS = None
        cls.get_tacos_from_api()

    @classmethod
    def submit_order(cls, order: FullOrder):
        logger.debug('Submitting order to API!')

        response = cls.do_api_interaction(cls.POST,
                                          '/orders/full',
                                          params={'apiKey': cls.API_KEY},
                                          body_object=order.get_dict())

        try:
            order_dict = response.json()
            if order is None:
                raise TacoTuesdayApiError(f'Could not create order {order.get_dict()}!')
        except Exception as e:
            raise TacoTuesdayApiError(f'An unknown error occurred when creating a full order: {e}!')

    @classmethod
    def get_employee_by_slack_id(cls, slack_id: str) -> Employee:
        response = cls.do_api_interaction(cls.GET, f'/employees/{slack_id}', params={'apiKey': cls.API_KEY})

        try:
            employee_dict = cls.get_json_from_response(response)
            if employee_dict is None: raise NoSuchEmployeeError(slack_id)

            assert employee_dict['slackId'] == slack_id

            nick_name = None if 'nickName' not in employee_dict else employee_dict['nickName']

            return Employee(slack_id, employee_dict['firstName'], employee_dict['lastName'], nick_name, api_id=employee_dict['id'])
        except KeyError as e:
            logger.debug(f'KeyError: {e}')
            raise NoSuchEmployeeError(slack_id)
        except AssertionError:
            raise TacoTuesdayApiError(f'An employee with a different Slack ID was returned (wanted: {slack_id}, returned: {employee_dict["slackId"]})!')

    @classmethod
    def create_employee(cls, employee: Employee) -> Employee:
        response = cls.do_api_interaction(request_method=cls.POST,
                                          uri=f'/employees/',
                                          params={'apiKey': cls.API_KEY},
                                          body_object=employee.get_dict())

        try:
            assert response.status_code == HTTPStatus.CREATED

            employee_dict = cls.get_json_from_response(response)
            assert employee_dict['slackId'] == employee.slack_id
            assert employee_dict['firstName'] == employee.name.first_name
            assert employee_dict['lastName'] == employee.name.last_name

            logger.info(f'Created Employee: {employee}!')

            employee.api_id = employee_dict['id']

            return employee
        except AssertionError:
            raise TacoTuesdayApiError(f'Failed to create Employee. API Response: {response}, {response.content}')
