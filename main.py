from Game.Game import Game
from Player.ConsolePlayer import ConsolePlayer

players = [ConsolePlayer("Player 1"), ConsolePlayer("Player 2"), ConsolePlayer("Player 3")]

game = Game(players)
game.play()

