class Peso:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value == 1:
            return "1 peso"
        else:
            return f"{self.value} pesos"


def test1():
    assert str(Peso(1)) == "1 peso"
    assert str(Peso(2)) == "2 pesos"


def test2():
    assert Peso(1) == Peso(1)
