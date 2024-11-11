from decimal import Decimal


class CoinModel:

    def __init__(self, name: str, symbol: str) -> None:
        self._name: str = name
        self._symbol: str = symbol
        self._price: Decimal = Decimal(0)
        self._last_updated: int = 0
        self._day_high_price: Decimal = Decimal(0)
        self._day_low_price: Decimal = Decimal(0)

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def symbol(self):
        return self._symbol

    @property
    def price(self):
        return self._price

    @property
    def last_updated(self):
        return self._last_updated

    @property
    def day_high_price(self):
        return self._day_high_price

    @property
    def day_low_price(self):
        return self._day_low_price

    # Setters
    @price.setter
    def price(self, value: Decimal):
        if value is not None and not isinstance(value, Decimal):
            raise TypeError("Price must be a Decimal or None")
        self._price = value

    @symbol.setter
    def symbol(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError("Symbol must be a string or None")
        self._symbol = value

    @last_updated.setter
    def last_updated(self, value: int):
        if value is not None and not isinstance(value, int):
            raise TypeError("last_updated must be a int or None")
        self._last_updated = value

    @day_high_price.setter
    def day_high_price(self, value: Decimal):
        if value is not None and not isinstance(value, Decimal):
            raise TypeError("Day high price must be a Decimal or None")
        self._day_high_price = value

    @day_low_price.setter
    def day_low_price(self, value: Decimal):
        if value is not None and not isinstance(value, Decimal):
            raise TypeError("Day low price must be a Decimal or None")
        self._day_low_price = value

    def __repr__(self):
        return (f"CoinModel(name={self._name}, symbol={self._symbol}, "
                f"price={self._price}, day_high_price={self._day_high_price}, "
                f"day_low_price={self._day_low_price})")
