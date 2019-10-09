from lib.domain.employee import Employee
from lib.domain.taco import Taco
from loguru import logger
import os
import requests
import json

class TacoTuesdayApiHandler:
    API_BASE_URL = os.environ['TT_BASE_API_URL']
    API_KEY = os.environ['TT_API_KEY']

    TACOS = {}

    @classmethod
    def form_api_url(cls, extension):
        return f'{cls.API_BASE_URL}/{extension}'

    # TODO: Email when can't get Tacos
    @classmethod
    def get_tacos_from_api(cls):
        if cls.TACOS:
            return cls.TACOS

        r = requests.get(cls.form_api_url('/tacos'))
        assert r.content is not None

        # TODO: catch JSON error
        tacos = json.loads(r.content)
        logger.debug("Taco(s) received from API: ", tacos)
        for taco in tacos:
            logger.debug(f'Loading taco: {taco}')
            taco_type = taco['type']
            cls.TACOS[taco_type] = Taco(taco_type=taco_type, price=taco['price'])

        return cls.TACOS

    def submit_order(self, order):
        pass

    def get_employee_by_slack_id(self, slack_id: str) -> Employee:
        pass

    def __init__(self):
        self.get_tacos_from_api()
