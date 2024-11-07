from typing import List, Tuple
from argparse import ArgumentTypeError
import random

from Card import CardType, Colors
from Card.Card import Card
from Card.Cards import NumberCard, ChooseColorCard, Add2Card, SwapCard, SkipCard, Add4Card
from Player.Player import Player
from Player import StatusCodes


class Game:
    deck: List[Card]
    passed_deck: List[Card]
    players: List[Player]
    players_number: int

    def shuffle(self) -> None:
        new_deck = [None]*108
        indexes = list(range(len(self.deck)))

        for card in self.deck:
            i = random.randint(0, len(indexes)-1)
            new_deck[indexes[i]] = card
            del indexes[i]

        self.deck = new_deck

    def __init__(self, players: List[Player]):
        self.passed_deck = []

        if len(players) < 2 or len(players) > 14:
            raise ArgumentTypeError("Players count must be between 2 and 14")

        self.players = players
        self.players_number = len(players)
        self.deck = []

        for num in range(1, 10):
            self.deck.extend([NumberCard(num, Colors.RED),
                              NumberCard(num, Colors.BLUE),
                              NumberCard(num, Colors.GREEN),
                              NumberCard(num, Colors.YELLOW)]*2)

        self.deck.extend([NumberCard(0, Colors.RED),NumberCard(0, Colors.BLUE),
                          NumberCard(0, Colors.GREEN),NumberCard(0, Colors.YELLOW)])

        self.deck = [Add4Card(), ChooseColorCard()] * 4

        for color in Colors:
            self.deck.extend([Add2Card(color),
                              SkipCard(color),
                              SwapCard(color)]*2)

        self.shuffle()

        last_i = 0
        for i, player in enumerate(self.players, 1):
            player.append_cards(self.deck[last_i:i*7])
            last_i = i*7
        self.deck = self.deck[:self.players_number*7]

        # Для тестов
        # #------------------------
        #
        # self.players[0].hand_deck = [ChooseColorCard()]
        # self.players[1].hand_deck = [ChooseColorCard()]
        # self.players[2].hand_deck = [ChooseColorCard()]
        #
        # #------------------------

        self.passed_deck.append(self.deck.pop())

    @staticmethod
    def cycle_players(collection: List[Player]):
        while True:
            for i, card in enumerate(collection):
                yield i, collection[i]

    def change_order_of_move(self, index_last_player: int) -> None:
        right = self.players[:index_last_player + 1:-1]
        left = self.players[index_last_player::-1]
        player = self.players[index_last_player]

        self.players = left + right
        self.players.append(player)

    def replace_passed_card_into_deck(self) -> None:
        self.deck = self.passed_deck
        self.passed_deck = []
        self.shuffle()

    def exclude_player(self, index_player: int, place: int) -> None:
        player = self.players[index_player]

        if place == -1:
            print(f'Player {player.name} lost')
        else:
            print(f'Player {player.name} won and took {place} place')
        del self.players[index_player]

    def play(self):
        place = 1
        players_order = Game.cycle_players(self.players)
        player_index, current_player = next(players_order)
        selected_color = None
        is_player_skipped = False
        is_taked_card = False

        while len(self.players) > 1:
            current_card = self.passed_deck[-1]

            print(f"Current card: {str(current_card)}")

            if selected_color is not None:
                print(f"Selected color: {str(selected_color.name)}")

            if current_card.type in [CardType.ADD4, CardType.SKIP, CardType.ADD2] and not is_player_skipped:
                card_index = -1
                card = NumberCard(1, Colors.RED)
            else:
                card_index, card = current_player.get_card_move(is_taked_card)

            if card_index == -2 and is_taked_card:
                is_player_skipped = False
                player_index, current_player = next(players_order)
                continue

            passed_card, isUno, isWin, status, out_color = current_player.make_move(
                (card_index, card),
                current_card,
                self.deck,
                selected_color,
                is_player_skipped
            )

            if isWin:
                if passed_card.type in [CardType.ADD4, CardType.CHOOSE_COLOR]:
                    selected_color = current_player.get_color_move()

                self.exclude_player(player_index, place)
                player_index, current_player = next(players_order)
                place += 1
                self.passed_deck.append(passed_card)
                is_player_skipped = False
                is_taked_card = False
                continue

            match status:
                case StatusCodes.NO_ERROR:
                    if passed_card is None:
                        is_taked_card = False
                        is_player_skipped = True
                        player_index, current_player = next(players_order)
                    else:
                        self.passed_deck.append(passed_card)
                        is_player_skipped = False
                        is_taked_card = False

                        if passed_card.type in [CardType.ADD4, CardType.CHOOSE_COLOR]:
                            selected_color = current_player.get_color_move()
                        else:
                            selected_color = None

                        if passed_card.type == CardType.SWAP:
                            self.change_order_of_move(player_index)
                            players_order = Game.cycle_players(self.players)

                            next(players_order)
                        player_index, current_player = next(players_order)
                case StatusCodes.TAKED_CARD:
                    is_taked_card = True
                case StatusCodes.NOT_ENOUGH_CARDS_IN_DECK:
                    self.replace_passed_card_into_deck()
                case StatusCodes.WRONG_CARD_CHOSEN:
                    print("Wrong card chosen")

        self.exclude_player(0, -1)



