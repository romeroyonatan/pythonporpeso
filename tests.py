class Unit(type):
    def __rmul__(self, other):
        return self(other)

    def __rtruediv__(self, other):
        # other: 120 * Peso
        # self: Dollar
        return ConversionRate(other, self)


class ConversionRate:
    def __init__(self, nominator, denominator):
        self.nominator = nominator  # pesos
        self.denominator = denominator  # dollar

    def multiply_currency(self, other):
        # self: convertion rate
        # other: 100 * Dollar
        # tengo que devolver pesos
        cls = type(self.nominator)
        return cls(other.value * self.nominator.value)

    def __rtruediv__(self, other):
        # self: conversion rate
        # other: 24000 * Peso
        # tengo que devolver dollar
        # nominador: pesos
        # denominador: Dollar
        return self.denominator(other.value / self.nominator.value)


class Currency(metaclass=Unit):
    singular: str
    plural: str

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.value == other.value

    def __str__(self):
        if self.value == 1:
            return f"{self.value} {self.singular}"
        else:
            return f"{self.value} {self.plural}"

    def __repr__(self):
        return f"{self.value} * {self.__class__.__name__}"

    def __add__(self, other):
        cls = type(self)
        if isinstance(other, cls):
            return cls(self.value + other.value)
        elif isinstance(other, Currency):
            return CurrencySum(self, other)
        else:
            return NotImplemented

    def __mul__(self, other):
        return other.multiply_currency(self)



class CurrencySum:
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2

    def __add__(self, other):
        if not isinstance(other, Currency):
            return NotImplemented
        return CurrencySum(self, other)

    def __str__(self):
        return f"{self.operand1} + {self.operand2}"

    def __repr__(self):
        return f"{repr(self.operand1)} + {repr(self.operand2)}"


class Peso(Currency):
    singular = "peso"
    plural = "pesos"


class Dollar(Currency):
    singular = "dollar"
    plural = "dollars"


class Euro(Currency):
    singular = "euro"
    plural = "euros"


def test1():
    assert str(Peso(1)) == "1 peso"
    assert str(Peso(2)) == "2 pesos"


def test2():
    assert Peso(1) == Peso(1)
    assert Peso(1) != Peso(2)


def test3():
    assert 1 * Peso == Peso(1)
    assert str(2 * Peso) == "2 pesos"


def test4():
    assert 1 * Dollar == Dollar(1)


def test5():
    assert 1 * Peso != 1 * Dollar


def test6():
    assert str(2 * Dollar) == "2 dollars"


def test7():
    conversion_rate = 120 * Peso / Dollar
    assert str(100 * Dollar * conversion_rate) == "12000 pesos"


def test8():
    conversion_rate = 120 * Peso / Dollar
    assert 24000 * Peso / conversion_rate == 200 * Dollar


def test9():
    assert repr(24000 * Peso) == "24000 * Peso"
    assert repr(240 * Dollar) == "240 * Dollar"


def test10():
    assert 1 * Euro == Euro(1)
    assert repr(24000 * Euro) == "24000 * Euro"
    assert str(24000 * Euro) == "24000 euros"
    assert str(1 * Euro) == "1 euro"


def test11():
    conversion_rate = 0.85 * Euro / Dollar
    assert 100 * Dollar * conversion_rate == 85 * Euro

    conversion_rate = 0.85 * Euro / Dollar
    assert 85 * Euro / conversion_rate == 100 * Dollar


def test12():
    assert 1 * Peso + 1 * Peso == 2 * Peso
    assert 1 * Euro + 1 * Euro == 2 * Euro


def test13():
    assert (
        str(10000 * Peso + 1000 * Dollar + 500 * Euro)
        == "10000 pesos + 1000 dollars + 500 euros"
    )
    assert (
            repr(10000 * Peso + 1000 * Dollar + 500 * Euro)
            == "10000 * Peso + 1000 * Dollar + 500 * Euro"
    )
