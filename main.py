from game import Game
from player import Player

players = [Player("Player1", [], 1000), Player("Player2", [], 1000), Player("Player3", [], 1000)]
game = Game(players)
game.play_hand()

