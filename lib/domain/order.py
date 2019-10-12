from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.domain.price import Price


class Order:
    TACOS = TacoTuesdayApiHandler.get_tacos_from_api()

    def __init__(self):
        self.price = Price()
        self.tacos = {}

    def _get_tacos(self, taco_type: str):
        if taco_type not in self.tacos:
            raise ValueError(f'No tacos of type {taco_type} in order!')

        return self.tacos[taco_type]

    def get_tacos(self):
        return self.tacos

    def add(self, taco_type: str, count: int):
        # TODO: Throw
        if count <= 0:
            return

        price = self.TACOS[taco_type].price
        if taco_type not in self.tacos:
            self.tacos[taco_type] = 0

        self.tacos[taco_type] += count
        self.price += count * price

    def __str__(self):
        # '4 Barbacoa, 3 Tripa, 4 Lengua, 2 Chicken Fajita - *$18.42*'
        return ', '.join([f'{self._get_tacos(t)} {self.TACOS[t].taco_type}' for t in self.tacos]) + f' - *{str(self.price)}*'
