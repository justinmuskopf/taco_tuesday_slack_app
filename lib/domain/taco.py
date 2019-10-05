from decimal import Decimal, ROUND_HALF_UP


class Taco:
    CENTS_PATTERN = Decimal('0.01')

    def __init__(self, taco_type: str, price: float):
        self.taco_type = taco_type
        self.price = Decimal(price)

    def get_price_string(self) -> str:
        return '${}'.format(self.price.quantize(self.CENTS_PATTERN, ROUND_HALF_UP))

