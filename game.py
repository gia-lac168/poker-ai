from deck import Deck

class Game:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.pot = 0
        self.highest_bet = 0
        self.current_round = 0

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

    def betting_round(self):
        # reset bets for new round
        for player in self.players:
            player.total_bet_this_round = 0

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

                if player.total_bet_this_round == self.highest_bet:  # skip player that is already match the bet
                    continue

                print(f"{player.name}'s turn")
                print(f"Your hole cards: {player.hole_cards}")
                print(f"Your chips: {player.chips}")
                print("Please select an action:")
                print("1. Fold")
                print("2. Call")
                print("3. Raise")
                decision = input("Your decision?: ")
                if decision == "1": #fold
                    print("Fold\n")
                    player.is_folded = True

                elif decision == "2": #call
                    print("Call\n")
                    amount_to_call = min(self.highest_bet - player.total_bet_this_round, player.chips)
                    player.chips -= amount_to_call
                    self.pot += amount_to_call
                    player.total_bet_this_round += amount_to_call

                elif decision == "3":
                    print("Raise")
                    player.amount_bet = int(input("How much would you like to raise to?: "))
                    print("")
                    while player.amount_bet > player.chips + player.total_bet_this_round:
                        print("You don't have enough chips! Please try again.")
                        player.amount_bet = int(input("How much would you like to raise to?: "))
                        print("")
                    someone_raised = True
                    self.highest_bet = player.amount_bet
                    player.chips -= self.highest_bet - player.total_bet_this_round
                    self.pot += self.highest_bet - player.total_bet_this_round
                    player.total_bet_this_round = self.highest_bet

                if player.chips == 0:
                    player.is_all_in = True
                    print("All in!\n")

    def play_hand(self):
        self.deal_hole_cards()
        self.highest_bet = 10  # starting bet (big blind placeholder)
        self.betting_round() #pre-flop
        self.current_round += 1
        self.deal_community_cards() #flop
        self.betting_round()
        self.deal_community_cards() #turn
        self.betting_round()
        self.deal_community_cards() #river
        self.betting_round()

