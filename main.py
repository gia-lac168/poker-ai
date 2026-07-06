from game import Game
from player import Player

players = [
    Player("Player1", [], 1000),              # human
    Player("Player2", [], 1000, is_bot=True),  # bot
    Player("Player3", [], 1000, is_bot=True),  # bot
]

game = Game(players)
game.play_hand()
