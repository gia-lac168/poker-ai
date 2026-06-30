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
someone_raised = True
current_bet = 10

while someone_raised:
    someone_raised = False
    for player in players:
        if player.is_folded: #skip player that is already folded
            continue

        if player.total_bet_this_round == current_bet: #skip player that is already match the bet
            continue

        print(f"{player.name}'s turn")
        print("Please select an action:")
        print("1. Fold")
        print("2. Call")
        print("3. Raise")
        decision = input("Your decision?: ")
        if decision == "1":
            print("Fold\n")
            player.is_folded = True

        elif decision == "2":
            print("Call\n")
            player.chips -= current_bet - player.total_bet_this_round
            pot += current_bet - player.total_bet_this_round
            player.total_bet_this_round = current_bet

        elif decision == "3":
            print("Raise")
            someone_raised = True
            player.amount_bet = int(input("How much would you like to raise to?: "))
            print("")
            current_bet = player.amount_bet
            player.chips -= current_bet - player.total_bet_this_round
            pot += current_bet - player.total_bet_this_round
            player.total_bet_this_round = current_bet

for player in players:
    print(f"{player.name}: chips={player.chips}, total_bet={player.total_bet_this_round}, folded={player.is_folded}")
print(f"\n Total pot: {pot}")