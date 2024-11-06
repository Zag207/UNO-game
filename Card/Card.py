from . import CardType, Colors
from abc import ABC, abstractmethod


class Card(ABC):
    type: CardType

    def __init__(self, card_type: CardType):
        self.type = card_type

    @abstractmethod
    def __str__(self) -> str:
        ...

