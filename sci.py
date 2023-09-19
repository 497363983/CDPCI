
operator = ['/', '^', '*', '**']


class unit:

    def __init__(self, unit: str = None, numerator: list | str = None, denominator: list | str = None) -> None:
        if unit:
            self.origin = unit


class sci_number:

    def __init__(self, value: int | float, unit: str | unit) -> None:
        self.value = value
        self.unit = unit

    def __str__(self) -> str:
        return f"{self.value} {self.unit}"

    def __add__(self, other):
        assert type(other) == sci_number, "sci_number must add sci_number"
        return self.add(other)

    def add(self, other):
        assert type(other) == sci_number, "sci_number must add sci_number"
        if self.unit == other.unit:
            return sci_number(self.value + other.value, self.unit)
        else:
            pass
