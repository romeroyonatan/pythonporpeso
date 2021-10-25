class Unit(type):
    def __rmul__(self, other):
        return self(other)

    def __rtruediv__(self, other):
        # other: 120 * Peso
        # self: Dollar
        return ConversionRate(other, self)


class ConversionRate:
    def __init__(self, nominator, denominator):
        self.nominator = nominator # pesos
        self.denominator = denominator # dollar

    def __rmul__(self, other):
        # self: convertion rate
        # other: 100 * Dollar
        # tengo que devolver pesos
        cls = type(self.nominator)
        return cls(other.value * self.nominator.value)


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


class Peso(Currency):
    singular = "peso"
    plural = "pesos"


class Dollar(Currency):
    singular = "dollar"
    plural = "dollars"


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
