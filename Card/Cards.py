from argparse import ArgumentTypeError

from Card.Card import Card
from . import CardType, Colors


class NumberCard(Card):
    number: int
    color: Colors

    def __init__(self, number: int, color: Colors):
        if 0 > number or number > 9:
            raise ArgumentTypeError("Number must be between 0 and 9")

        self.number = number
        self.color = color
        super().__init__(CardType.NUMBER)

    def __str__(self) -> str:
        str_card_color = str_card_number = ""

        if self.color is not None:
            str_card_color = self.color.name
        if self.number is not None:
            str_card_number = str(self.number)

        return f"{self.type.name} {str_card_color} {str_card_number}"


class SwapCard(Card):
    color: Colors

    def __init__(self, color: Colors):
        self.color = color
        super().__init__(CardType.SWAP)

    def __str__(self) -> str:
        str_card_color = ""

        if self.color is not None:
            str_card_color = self.color.name

        return f"{self.type.name} {str_card_color}"


class SkipCard(Card):
    color: Colors

    def __init__(self, color: Colors):
        self.color = color
        super().__init__(CardType.SKIP)

    def __str__(self) -> str:
        str_card_color = ""

        if self.color is not None:
            str_card_color = self.color.name

        return f"{self.type.name} {str_card_color}"


class Add2Card(Card):
    color: Colors

    def __init__(self, color: Colors):
        self.color = color
        super().__init__(CardType.ADD2)

    def __str__(self) -> str:
        str_card_color = ""

        if self.color is not None:
            str_card_color = self.color.name

        return f"{self.type.name} {str_card_color}"


class ChooseColorCard(Card):
    def __init__(self):
        super().__init__(CardType.CHOOSE_COLOR)

    def __str__(self) -> str:
        return f"{self.type.name}"


class Add4Card(Card):
    def __init__(self):
        super().__init__(CardType.ADD4)

    def __str__(self) -> str:
        return f"{self.type.name}"
