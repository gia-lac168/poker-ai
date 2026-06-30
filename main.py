from deck import Deck
from player import Player

my_deck = Deck()
my_deck.shuffle()

players = [Player("Player1", [], 1000), Player("Player2", [], 1000), Player("Player3", [], 1000)]

for player in players:
    player.hole_cards = [my_deck.deal(), my_deck.deal()]

community_cards = []

#burn 1 card + flop
my_deck.deal()
for _ in range(3):
    community_cards.append(my_deck.deal())

#burn 1 card + turn
my_deck.deal()
community_cards.append(my_deck.deal())

#burn 1 card + river
my_deck.deal()
community_cards.append(my_deck.deal())

pot = 0
for player in players:
    print("Please select an action:")
    print("1. Fold")
    print("2. Call")
    decision = input("Your decision?: ")
    if decision == "1":
        print("Fold\n")
        player.is_folded = True
    else:
        print("Call\n")
        player.chips -= 10
        pot += 10
