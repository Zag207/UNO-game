from enum import Enum


class Colors(Enum):
    RED = 'r'
    GREEN = 'g'
    BLUE = 'b'
    YELLOW = 'y'


class CardType(Enum):
    NUMBER = 'number'
    SWAP = "swap"
    SKIP = "skip"
    ADD2 = "add2"
    CHOOSE_COLOR = "choice_color"
    ADD4 = "add4"
