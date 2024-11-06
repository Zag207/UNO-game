from typing import List, Tuple, NoReturn
from abc import ABC, abstractmethod

from Card.Card import Card
from Card import CardType, Colors
from Player import StatusCodes


class Player(ABC):
    name: str
    hand_deck: List[Card]

    def __init__(self, name: str, cards: List[Card] | None = None):
        self.name = name

        if cards is None:
            self.hand_deck = []
        else:
            self.hand_deck = cards

    def append_cards(self, cards: List[Card]) -> None:
        self.hand_deck.extend(cards)

    @abstractmethod
    def get_card_move(self, is_taked_card: bool) -> Tuple[int, Card | None]:
        raise NotImplementedError

    @abstractmethod
    def get_color_move(self) -> Colors:
        raise NotImplementedError

    def __str__(self) -> str:
        def foo(obj: Tuple[int, Card]) -> str:
            return str(obj[0]) + " - " + str(obj[1])

        return f"{self.name}\nDeck: \n{'\n'.join([foo(x) for x in enumerate(self.hand_deck)])}"

    def make_move(
            self,
            move: Tuple[int, Card | None],
            input_card: Card, deck: List[Card],
            input_color: Colors | None = None,
            is_previous_player_skipped: bool = False
    ) -> Tuple[Card | None, bool, bool, StatusCodes, Colors | None]:
        """
        Returns: used_card, isUNO, isWIN, StatusCode, output_color
        """

        def take_cards(card_count_for_take: int) -> Tuple[Card | None, bool, bool, StatusCodes, Colors | None]:
            if len(deck) < card_count_for_take:
                return (None, len(self.hand_deck) == 1, len(self.hand_deck) == 0,
                        StatusCodes.NOT_ENOUGH_CARDS_IN_DECK, None)
            else:
                self.append_cards([deck.pop() for _ in range(card_count_for_take)])

                if card_count_for_take == 1:
                    return (None, len(self.hand_deck) == 1, len(self.hand_deck) == 0,
                            StatusCodes.TAKED_CARD, None)

                return (None, len(self.hand_deck) == 1, len(self.hand_deck) == 0,
                        StatusCodes.NO_ERROR, None)

        def process_card(chosen_card: Card, condition) -> NoReturn:
            if condition(chosen_card):
                del self.hand_deck[card_index]

                return chosen_card, len(self.hand_deck) == 1, len(self.hand_deck) == 0, StatusCodes.NO_ERROR, None

            return None, len(self.hand_deck) == 1, len(self.hand_deck) == 0, StatusCodes.WRONG_CARD_CHOSEN, None

        card_index, chosen_card = move

        if chosen_card is None:
            return take_cards(1)

        match input_card.type:
            case CardType.NUMBER:
                return process_card(chosen_card,
                             lambda card: card.type in [CardType.CHOOSE_COLOR, CardType.ADD4] or
                                          card.color == input_card.color or
                                          card.type == CardType.NUMBER and card.number == input_card.number)

            case CardType.SWAP:
                return process_card(chosen_card,
                             lambda card: card.type in [CardType.CHOOSE_COLOR, CardType.ADD4] or
                                          card.color == input_card.color or card.type == CardType.SWAP)

            case CardType.ADD2:
                if not is_previous_player_skipped:
                    return take_cards(2)
                else:
                    return process_card(chosen_card,
                                 lambda card: card.type in [CardType.CHOOSE_COLOR, CardType.ADD4] or
                                                card.color == input_card.color or card.type == CardType.ADD2)

            case CardType.SKIP:
                if not is_previous_player_skipped:
                    return (None, len(self.hand_deck) == 1, len(self.hand_deck) == 0,
                        StatusCodes.NO_ERROR, None)
                else:
                    return process_card(chosen_card,
                                 lambda card: card.type in [CardType.CHOOSE_COLOR, CardType.ADD4] or
                                            card.color == input_card.color or card.type == CardType.SKIP)

            case CardType.CHOOSE_COLOR:
                return process_card(chosen_card,
                             lambda card: card.type in [CardType.CHOOSE_COLOR, CardType.ADD4] or
                                            card.color == input_color)

            case CardType.ADD4:
                if not is_previous_player_skipped:
                    return take_cards(4)
                else:
                    return process_card(chosen_card,
                                 lambda card: card.type in [CardType.CHOOSE_COLOR, CardType.ADD4] or
                                            card.color == input_color)
