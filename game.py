from deck import Deck
from evaluator import evaluate_hand
from itertools import combinations
from montecarlo import estimate_win_probability
from ai import bot_action

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
        self.current_round += 1

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
        print(f"DEBUG: pot after blinds = {self.pot}")

    def betting_round(self, starting_bet=0):
        print(f"DEBUG: pot at start of betting_round = {self.pot}")
        raise_count = 0
        max_raises = 4
        self.highest_bet = starting_bet

        if starting_bet == 0:  # post-flop — reset bets
            for player in self.players:
                player.total_bet_this_round = 0

        acted = set()

        # show game state
        print("\n========== GAME STATE ==========")
        if self.community_cards:
            print(f"Community cards: {self.community_cards}")
        else:
            print("Community cards: None yet (pre-flop)")
        print(f"Pot: {self.pot}")
        print("================================\n")

        someone_raised = True

        while someone_raised:
            someone_raised = False
            for player in self.players:
                if player.is_folded or player.is_all_in:  # skip player that is already folded or all-in
                    continue

                if player.name in acted and player.total_bet_this_round == self.highest_bet:  # skip player that is already match the bet
                    continue

                #player's information
                print(f"{player.name}'s turn")
                print(f"Your hole cards: {player.hole_cards}")
                print(f"Current bet: {self.highest_bet}")
                print(f"Your chips: {player.chips}")

                #bot action
                if player.is_bot:
                    current_pot = self.pot + sum(p.total_bet_this_round for p in self.players)
                    active_opponents = len([p for p in self.players if not p.is_folded and p != player])
                    action, amount = bot_action(player, self.highest_bet, self.community_cards, active_opponents, current_pot)

                    # execute the action
                    if action == "Fold":
                        print(f"{player.name} folded\n")
                        player.is_folded = True

                    elif action == "Call" or action == "Check":
                        if self.highest_bet == 0:
                            print(f"{player.name} check\n")
                        else:
                            print(f"{player.name} call\n")
                        amount_to_call = min(self.highest_bet - player.total_bet_this_round, player.chips)
                        player.chips -= amount_to_call
                        self.pot += amount_to_call
                        player.total_bet_this_round += amount_to_call

                    elif action == "Raise":
                        print(f"{player.name} raise\n")
                        if raise_count >= max_raises:
                            # force call instead
                            amount_to_call = min(self.highest_bet - player.total_bet_this_round, player.chips)
                            player.chips -= amount_to_call
                            self.pot += amount_to_call
                            player.total_bet_this_round += amount_to_call
                            print(f"{player.name} call (raise cap reached)\n")
                        else:
                            raise_count += 1
                            player.amount_bet = amount
                            print(f"{player.name} raise to {player.amount_bet}\n")
                            someone_raised = True
                            self.highest_bet = player.amount_bet
                            player.chips -= self.highest_bet - player.total_bet_this_round
                            self.pot += self.highest_bet - player.total_bet_this_round
                            player.total_bet_this_round = self.highest_bet

                else: #player action
                    #Estimated win probability
                    prob = estimate_win_probability(player.hole_cards, self.community_cards, len([p for p in self.players if not p.is_folded and p != player]), )
                    print(f"Estimated win probability: {prob:.1%}")

                    #Option menu
                    print("Please select an action:")
                    print("1. Fold")
                    if self.highest_bet == 0:
                        print("2. Check")
                    else:
                        print("2. Call")
                    print("3. Raise")
                    decision = input("Your decision?: ")

                    if decision == "1": #fold
                        print(f"{player.name} folded\n")
                        player.is_folded = True

                    elif decision == "2": #call
                        if self.highest_bet == 0:
                            print(f"{player.name} check\n")
                        else:
                            print(f"{player.name} call\n")
                        amount_to_call = min(self.highest_bet - player.total_bet_this_round, player.chips)
                        player.chips -= amount_to_call
                        self.pot += amount_to_call
                        player.total_bet_this_round += amount_to_call

                    elif decision == "3":
                        print(f"{player.name} raise\n")
                        player.amount_bet = int(input("How much would you like to raise to?: "))
                        print("")

                        #check if the raise is valid
                        while player.amount_bet <= self.highest_bet or player.amount_bet > player.chips + player.total_bet_this_round:
                            if player.amount_bet <= self.highest_bet:
                                print(f"Raise must be higher than current bet of {self.highest_bet}. Please try again.")
                            else:
                                print("You don't have enough chips! Please try again.")
                            player.amount_bet = int(input("How much would you like to raise to?: "))

                        someone_raised = True
                        print(f"{player.name} raise to {player.amount_bet}\n")
                        self.highest_bet = player.amount_bet
                        player.chips -= self.highest_bet - player.total_bet_this_round
                        self.pot += self.highest_bet - player.total_bet_this_round
                        player.total_bet_this_round = self.highest_bet

                if player.chips <= 0:
                    player.chips = 0  # prevent negative chips
                    player.is_all_in = True
                    print("All in!\n")

                acted.add(player.name)

                if len(self.active_players()) == 1:
                    winner = self.active_players()[0]
                    print(f"\n{winner.name} wins the pot of {self.pot} chips (everyone else folded)!")
                    winner.chips += self.pot
                    return True  # signal that hand is over

    def active_players(self):
        return [p for p in self.players if not p.is_folded]

    def showdown(self):
        winner = None
        highest_player_score = (-1,)

        for player in self.players:
            if player.is_folded:
                continue
            all_cards = self.community_cards + player.hole_cards
            all_5_cards_hand = list(combinations(all_cards, 5))
            player_best_hand = None
            player_best_score = (-1,)

            for hand in all_5_cards_hand:
                score = evaluate_hand(hand)

                if score > player_best_score:
                    player_best_score = score
                    player_best_hand = hand

            if player_best_score > highest_player_score:
                winner = player.name
                highest_player_score = player_best_score

        for player in self.players:
            if player.name == winner:
                player.chips += self.pot
                break
        print(f"{winner} won this round and collected {self.pot} chips!")

    def play_hand(self):
        # reset bets for new round
        for player in self.players:
            player.total_bet_this_round = 0

        self.deal_hole_cards()
        self.post_blinds()
        if self.betting_round(starting_bet = self.big_blind): # pre-flop
            return
        self.current_round += 1
        self.deal_community_cards() #flop
        if self.betting_round():
            return
        self.deal_community_cards() #turn
        if self.betting_round():
            return
        self.deal_community_cards() #river
        if self.betting_round():
            return
        self.showdown()
        self.dealer = (self.dealer + 1) % len(self.players) #move the dealer's index
