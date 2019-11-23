import os
import sys

from config.order_config import TacoTuesdayOrderConfig
from lib.domain.domain_error import DomainError
from lib.domain.price import Price
from lib.domain.taco import Taco, NegativeTacoError, ValidTacos, TacoValueError, InvalidTacoTypeError


class OrderError(DomainError):
    def __init__(self, message: str):
        super().__init__(Order, message)


class TacoCountError(OrderError):
    def __init__(self, taco_type: str, taco_count: int = 0, needed: int = 0):
        if taco_count == 0 and needed == 0:
            super().__init__(f'No Tacos of type {taco_type} in order!')

        super().__init__(f'Invalid number of {taco_type} tacos in order: (Have: {taco_count}, Need: {needed})!')

    @classmethod
    def assert_have_at_least(cls, taco_type: str, have: int, need: int):
        if need > have: raise cls(taco_type, have, need)


class Order:
    TAX_RATE: float = 1 + (float(TacoTuesdayOrderConfig().get_tax_rate()) / 100)

    def __init__(self):
        self.price = Price()
        self.deal_price = Price()
        self.tacos = {t: 0 for t in ValidTacos.get_tacos()}

    def __getitem__(self, taco_type: str):
        return self.get_tacos(taco_type)

    def __iter__(self):
        for taco_type in self.tacos: yield taco_type

    @staticmethod
    def _get_price_for_tacos(taco_type: str, count: int):
        return ValidTacos.get_taco_price(taco_type).price * count

    @staticmethod
    def _is_valid_count(count):
        NegativeTacoError.assert_non_negative(count)
        return count > 0

    @staticmethod
    def get_taco_name(taco_type: str):
        return ValidTacos.get_taco(taco_type).name

    def get_tacos(self, taco_type: str) -> int:
        InvalidTacoTypeError.assert_type_valid(taco_type)
        return self.tacos[taco_type]

    def _is_valid_taco_change(self, taco_type: str, count: int, adding: bool):
        InvalidTacoTypeError.assert_type_valid(taco_type)
        if not self._is_valid_count(count): return False
        if adding: return True

        TacoCountError.assert_have_at_least(taco_type, self.tacos[taco_type], count)
        return True

    def add(self, taco_type: str, count: int):
        if not self._is_valid_taco_change(taco_type, count, True): return

        if taco_type not in self.tacos:
            self.tacos[taco_type] = 0

        self.tacos[taco_type] += count

        # Exclude Pastor for later when calculating deal
        if not Taco.is_pastor(taco_type):
            taco_price = self._get_price_for_tacos(taco_type, count)
            self.price += taco_price

    def remove(self, taco_type: str, count: int):
        if not self._is_valid_taco_change(taco_type, count, False): return

        if taco_type not in self.tacos:
            raise TacoCountError(taco_type)

        self.tacos[taco_type] -= count

        if not Taco.is_pastor(taco_type):
            taco_price = self._get_price_for_tacos(taco_type, count)
            self.price -= taco_price

    def remove_taco_type(self, taco_type: str):
        self.remove(taco_type, self.tacos[taco_type])

    def _get_price_based_on_deal(self, pastor_price: float):
        pastor_total = self.tacos['pastor'] * pastor_price

        return round((self.price + pastor_total) * self.TAX_RATE, 2)

    def get_dict(self, pastor_price: float) -> {}:
        d = {t: self.tacos[t] for t in self.tacos}
        d['total'] = self._get_price_based_on_deal(pastor_price).get()

        return d

    def get_order_string(self, pastor_price: float):
        # ['4 Barbacoa', '3 Tripa', '4 Lengua', '2 Chicken Fajita']
        taco_number_strings = []
        for taco_type in self.tacos:
            if self.tacos[taco_type] == 0: continue
            taco_number_strings.append(f'{self.tacos[taco_type]} {self.get_taco_name(taco_type)}')

        # '4 Barbacoa, 3 Tripa, 4 Lengua, 2 Chicken Fajita - *$18.42*'
        return ', '.join(taco_number_strings) + f' - *{self._get_price_based_on_deal(pastor_price)}*'
