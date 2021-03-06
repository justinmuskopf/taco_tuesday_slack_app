import copy
from decimal import Decimal, ROUND_HALF_UP
from loguru import logger

from lib.domain.domain_error import DomainError, DomainValueError
from lib.domain.price import Price


class TacoError(DomainError):
    def __init__(self, message: str):
        super().__init__(Taco, message)


class TacoValueError(DomainValueError):
    def __init__(self, key: str, value):
        super().__init__(Taco, key, value)


class NegativeTacoError(TacoValueError):
    def __init__(self, count: int):
        super().__init__('count', count)

    @classmethod
    def assert_non_negative(cls, count: int):
        if count < 0: raise cls(count)


class InvalidTacoTypeError(TacoValueError):
    def __init__(self, taco_type: str):
        super().__init__('taco_type', taco_type)

    @classmethod
    def assert_type_valid(cls, taco_type: str):
        if not ValidTacos.is_valid_taco_type(taco_type): raise cls(taco_type)


class Taco:
    def __init__(self, taco_type: str, name: str, price: float):
        self.taco_type = taco_type
        self.name = name
        self.price = Price(price)

    def copy(self):
        return Taco(self.taco_type, self.price.get())

    @staticmethod
    def is_pastor(taco_type: str):
        return taco_type == 'pastor'

    def __str__(self):
        return f'{self.name} ({str(self.price)})'


class ValidTacos:
    VALID_TACOS: {str: Taco} = None

    @classmethod
    def _assert_tacos_initialized(cls):
        if cls.VALID_TACOS is None: raise TacoError('No Valid Tacos have been defined!')

    @classmethod
    def _assert_valid_taco_type(cls, taco_type: str):
        cls._assert_tacos_initialized()
        InvalidTacoTypeError.assert_type_valid(taco_type)

    @classmethod
    def set_tacos(cls, valid_tacos: {str, Taco}):
        cls.VALID_TACOS = valid_tacos

    @classmethod
    def get_tacos(cls) -> {str: Taco}:
        cls._assert_tacos_initialized()
        return copy.deepcopy(cls.VALID_TACOS)

    @classmethod
    def is_valid_taco_type(cls, taco_type: str) -> bool:
        return taco_type in cls.VALID_TACOS

    @classmethod
    def get_taco(cls, taco_type: str) -> Taco:
        InvalidTacoTypeError.assert_type_valid(taco_type)

        return copy.deepcopy(cls.VALID_TACOS[taco_type])

    @classmethod
    def get_taco_price(cls, taco_type: str) -> Price:
        cls._assert_valid_taco_type(taco_type)

        return cls.get_taco(taco_type).price
