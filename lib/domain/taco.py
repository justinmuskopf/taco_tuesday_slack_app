from decimal import Decimal, ROUND_HALF_UP
from loguru import logger

from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.domain.price import Price


class TacoError(ValueError):
    VALID_TACOS = TacoTuesdayApiHandler.get_tacos_from_api()

    def __init__(self, taco_type: str = '', count: int = 0):
        err = 'An unknown TacoError occurred!'

        # TODO: ¿por qué no los dos?
        if taco_type:
            err = f'Invalid Taco Type: "{taco_type}". Valid tacos: {self.VALID_TACOS})'
        elif count < 0:
            err = f'Given a negative number of tacos! ({count})'

        logger.error(err)
        super().__init__(err)


class Taco:
    def __init__(self, taco_type: str, price: float):
        self.taco_type = self.deserialize_type(taco_type)
        self.price = Price(price)

    @staticmethod
    def serialize_type(taco_type: str) -> str:
        serialized = taco_type.replace(' ', '_').upper()
        logger.debug(f'Taco Type: {taco_type} --> {serialized}')

        return serialized

    @staticmethod
    def deserialize_type(taco_type: str) -> str:
        words = [w[0].upper() + w[1:].lower() for w in taco_type.split('_')]
        deserialized = ' '.join(words)
        logger.debug(f'Taco Type: {taco_type} --> {deserialized}')

        return deserialized

    def __str__(self):
        return f'{self.taco_type} ({str(self.price)})'
