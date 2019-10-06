from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.domain.taco import Taco


class IndividualOrder:
    TACOS = TacoTuesdayApiHandler.get_tacos_from_api()

    def __init__(self):
        self.price: float = 0
        self.tacos = {}

    def add(self, taco_type: str, count: int):
        # TODO: Throw
        if count <= 0:
            return

        price = self.TACOS[taco_type]['price']
        if taco_type not in self.tacos:
            self.tacos[taco_type] = 0

        self.tacos[taco_type] += count
        self.price += count * price
