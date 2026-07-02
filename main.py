from game import Game
from player import Player


#TODO: replace hardcoded players with dynamic user input later
players = [Player("Player1", [], 1000), Player("Player2", [], 1000), Player("Player3", [], 1000)]
game = Game(players)
game.play_hand()
