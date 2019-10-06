from decimal import Decimal, ROUND_HALF_UP
from loguru import logger


class Taco:
    CENTS_PATTERN = Decimal('0.01')

    def __init__(self, taco_type: str, price: float):
        self.taco_type = self.deserialize_type(taco_type)
        self.price = Decimal(price)

    def get_price_string(self) -> str:
        return '${}'.format(self.price.quantize(self.CENTS_PATTERN, ROUND_HALF_UP))

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
