from typing import Tuple, List

from Card import Colors
from Card.Card import Card
from .Player import Player


class ConsolePlayer(Player):
    def __init__(self, name: str, cards: List[Card] | None = None):
        super().__init__(name, cards)

    def get_card_move(self, is_taked_card: bool) -> Tuple[int, Card | None]:
        def validate_card_choose(choose_str: str) -> int:
            try:
                validated_card_choose = int(choose_str)
            except ValueError:
                return -1

            if 0 <= validated_card_choose < len(self.hand_deck):
                return validated_card_choose
            else:
                return -1

        print(f"Player: {self.name}")

        action = ""
        print('\n'.join([f"{str(x[0])} - {str(x[1])}" for x in enumerate(self.hand_deck)]), end="\n\n")
        while not (action == "1" and (not is_taked_card) or action == "2" or action == "3" and is_taked_card):
            action = input("Select an action:\n1 - Take a card\n2 - Play a card\n3 - Skip move\n>> ")

        if action == "1":
            return -1, None
        elif action == "3":
            return -2, None
        else:
            card_selected = ""

            while validate_card_choose(card_selected) == -1:
                print('\n'.join([f"{str(x[0])} - {str(x[1])}" for x in enumerate(self.hand_deck)]), end="\n\n")
                card_selected = input("Select a card to play:\n>> ")

            card_index = validate_card_choose(card_selected)

            return card_index, self.hand_deck[card_index]

    def get_color_move(self) -> Colors:
        selected_color = ""
        colors = [str(color.name).lower() for color in Colors]

        while selected_color not in colors:
            print("Select a color")
            print(f"Colors: " + ", ".join(colors))
            selected_color = input(">> ")

        return Colors(selected_color[0])
