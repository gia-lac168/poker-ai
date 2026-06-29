class Player:
    def __init__(self, name, hole_cards, chips):
        self.name = name
        self.hole_cards = hole_cards
        self.chips = chips
        self.current_bet = 0
        self.total_bet_this_round = 0
        self.is_folded = False
        self.is_all_in = False

from deck import Deck

my_deck = Deck()
my_deck.shuffle()

players = [Player("Player1", [], 1000), Player("Player2", [], 1000), Player("Player3", [], 1000)]

for player in players:
    player.hole_cards = [my_deck.deal(), my_deck.deal()]