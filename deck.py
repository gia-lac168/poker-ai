class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f'{self.rank}{self.suit}'

import random

class Deck:
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["♠", "♣", "♦", "♥"]

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()