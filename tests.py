class PesoMeta(type):
    def __rmul__(self, other):
        return Peso(other)


class Peso(metaclass=PesoMeta):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value == 1:
            return "1 peso"
        else:
            return f"{self.value} pesos"

    def __eq__(self, other):
        if not isinstance(other, Peso):
            return NotImplemented
        return self.value == other.value


def test1():
    assert str(Peso(1)) == "1 peso"
    assert str(Peso(2)) == "2 pesos"


def test2():
    assert Peso(1) == Peso(1)
    assert Peso(1) != Peso(2)


def test3():
    assert 1 * Peso == Peso(1)
    assert str(2 * Peso) == "2 pesos"
