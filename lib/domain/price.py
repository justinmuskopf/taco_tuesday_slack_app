from decimal import Decimal,ROUND_HALF_UP


class Price:
    CENTS_PATTERN = Decimal('0.01')

    def __init__(self, price: float = 0):
        self.price = Decimal(price)

    def add(self, price: float):
        self.price += Decimal(price)

    def get(self):
        return self.price.quantize(self.CENTS_PATTERN, ROUND_HALF_UP)

    def __add__(self, other):
        self.price += other

    def __str__(self):
        return f'${self.get()}'
