from lib.domain.taco import Taco
import os
import requests
import json


class TacoTuesdayApiHandler:
    API_BASE_URL = os.environ['TT_BASE_API_URL']
    API_KEY = os.environ['TT_API_KEY']

    TACOS = {}

    # TODO: Email when can't get Tacos
    @classmethod
    def get_tacos_from_api(cls):
        if cls.TACOS:
           return cls.TACOS

        r = requests.get(cls.API_BASE_URL + '/tacos')
        assert r.content is not None

        # TODO: catch JSON error
        tacos = json.loads(r.content)
        print("Taco(s) received from API: ", tacos)
        for taco in tacos:
            print(f'Loading taco: {taco}')
            taco_type = taco['type']
            cls.TACOS[taco_type] = Taco(taco_type=taco_type, price=taco['price'])

        return cls.TACOS

    def __init__(self):
        self.get_tacos_from_api()
