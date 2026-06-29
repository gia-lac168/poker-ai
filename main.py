from deck import Deck
from player import Player

my_deck = Deck()
my_deck.shuffle()

players = [Player("Player1", [], 1000), Player("Player2", [], 1000), Player("Player3", [], 1000)]

for player in players:
    player.hole_cards = [my_deck.deal(), my_deck.deal()]