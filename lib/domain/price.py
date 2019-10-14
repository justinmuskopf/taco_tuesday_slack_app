
class InvalidPriceError(ValueError):
    def __init__(self, message):
        super().__init__(message)

class Price:
    def __init__(self, price: float = 0):
        self.price = price

    def add(self, price: float):
        self.price += price

    def get(self):
        return self.price

    def __mul__(self, other):
        if other is None:
            raise InvalidPriceError('Cannot multiply by None!')

        t = type(other)
        if t is Price:
            self.price *= other.price
        if t is int or t is float:
            self.price *= other
        else:
            raise InvalidPriceError(f'Cannot multiply value {other}')

        return self

    def __add__(self, other):
        if other is None:
            raise InvalidPriceError('Cannot add None value to Price!')

        t = type(other)
        if t is Price:
            self.price += other.price
        elif t is int or t is float:
            self.price += other
        else:
            raise InvalidPriceError(f'Cannot add type {t} to Price!')

        return self

    def __str__(self):
        return format(self.price, '.2f')
