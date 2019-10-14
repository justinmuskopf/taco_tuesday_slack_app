from lib.domain.price import Price
from lib.domain.taco import Taco


class Order:
    TACOS: {str, Taco} = None

    @classmethod
    def set_taco_prices(cls, taco_prices):
        Order.TACOS = taco_prices

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

        if taco_type not in self.tacos:
            self.tacos[taco_type] = 0

        self.tacos[taco_type] += count
        self.price += Order.TACOS[taco_type].price * count

    def __str__(self):
        # '4 Barbacoa, 3 Tripa, 4 Lengua, 2 Chicken Fajita - *$18.42*'
        return ', '.join([f'{self._get_tacos(t)} {self.TACOS[t].taco_type}' for t in self.tacos]) + f' - *${self.price}*'
