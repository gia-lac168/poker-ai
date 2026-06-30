class Player:
    def __init__(self, name, hole_cards, chips):
        self.name = name
        self.hole_cards = hole_cards
        self.chips = chips
        self.amount_bet = 0
        self.total_bet_this_round = 0
        self.is_folded = False
        self.is_all_in = False