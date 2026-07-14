from deck import Deck
from evaluator import evaluate_hand
from itertools import combinations

class Game:
    def __init__(self, players, small_blind=5, big_blind=10):
        self.players = players
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.pot = 0
        self.highest_bet = 0
        self.current_round = 0
        self.dealer = 0 #index of dealer position
        self.small_blind = small_blind
        self.big_blind = big_blind

    def deal_hole_cards(self):
        for player in self.players:
            player.hole_cards = [self.deck.deal(), self.deck.deal()]

    def deal_community_cards(self):
        self.deck.deal() #burn 1 card
        if self.current_round == 1: #flop
             for _ in range(3):
                self.community_cards.append(self.deck.deal())
        else: #turn and river
            self.community_cards.append(self.deck.deal())

    def post_blinds(self):
        sb_index = (self.dealer + 1) % len(self.players)
        bb_index = (self.dealer + 2) % len(self.players)

        sb_player = self.players[sb_index]
        bb_player = self.players[bb_index]

        #post small blind player:
        sb_player.chips -= self.small_blind
        sb_player.total_bet_this_round = self.small_blind
        self.pot += sb_player.total_bet_this_round
        print(f"{sb_player.name} posts small blind: {self.small_blind}")

        # post big blind
        bb_player.chips -= self.big_blind
        bb_player.total_bet_this_round = self.big_blind
        self.pot += self.big_blind
        self.highest_bet = self.big_blind
        print(f"{bb_player.name} posts big blind: {self.big_blind}")

    def active_players(self):
        return [p for p in self.players if not p.is_folded]

    def showdown(self):
        winner = None
        highest_player_score = (-1,)

        for player in self.players:
            if player.is_folded:
                continue
            all_cards = self.community_cards + player.hole_cards
            player_best_score = max(evaluate_hand(list(hand)) for hand in combinations(all_cards, 5))

            if player_best_score > highest_player_score:
                winner = player
                highest_player_score = player_best_score

        winner.chips += self.pot
        return f"{winner.name} wins {self.pot} chips!"

    def start_hand(self):
        self.community_cards = []
        self.pot = 0
        self.current_round = 0
        self.highest_bet = 0
        self.deck = Deck()
        self.deck.shuffle()

        for player in self.players:
            player.hole_cards = []
            player.is_folded = False
            player.is_all_in = False
            player.has_acted = False
            player.total_bet_this_round = 0
            player.amount_bet = 0

        self.deal_hole_cards()
        self.post_blinds()

    def get_current_player(self):
        for player in self.players:
            if player.is_folded or player.is_all_in:  # skip player that is already folded or all-in
                continue

            if player.has_acted and player.total_bet_this_round == self.highest_bet:  # skip player that is already match the bet
                continue
            return player
        return None

    def process_action(self, player, action, amount=0):
        message = ""

        if action == "fold":
            player.is_folded = True
            message = f"{player.name} folded\n"

        elif action == "call":
            amount_to_call = min(self.highest_bet - player.total_bet_this_round, player.chips)
            player.chips -= amount_to_call
            self.pot += amount_to_call
            player.total_bet_this_round += amount_to_call
            if self.highest_bet == 0:
                message = f"{player.name} check\n"
            else:
                message = f"{player.name} called {amount_to_call}\n"

        elif action == "raise":
            self.highest_bet = amount
            player.chips -= amount - player.total_bet_this_round
            self.pot += amount - player.total_bet_this_round
            player.total_bet_this_round = amount

            # reset everyone else's has_acted so they get to respond
            for p in self.players:
                if p != player:
                    p.has_acted = False
            message = f"{player.name} raise to {amount}\n"

        player.has_acted = True

        if player.chips <= 0:
            player.chips = 0
            player.is_all_in = True
            message += "All in!\n"
        return message

    def advance_round(self):
        active = self.active_players()
        if len(active) == 1:
            winner = active[0]
            winner.chips += self.pot
            return "winner", f"{winner.name} wins {self.pot} chips!"

        # reset betting for new street
        self.highest_bet = 0
        for player in self.players:
            player.total_bet_this_round = 0
            player.has_acted = False

        self.current_round += 1

        if self.current_round == 1: #flop
            self.deal_community_cards()
            return "continue", "flop"
        elif self.current_round == 2: #turn
            self.deal_community_cards()
            return "continue", "turn"
        elif self.current_round == 3: #river
            self.deal_community_cards()
            return "continue", "river"
        else: #showdown
            result = self.showdown()
            return "winner", result


