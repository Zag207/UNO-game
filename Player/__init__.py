from enum import Enum


class StatusCodes(Enum):
    NO_ERROR = 0
    TAKED_CARD = 1
    NOT_ENOUGH_CARDS_IN_DECK = 2
    WRONG_CARD_CHOSEN = 3
