from deck import Deck
from evaluator import evaluate_hand
from itertools import combinations
import random

def estimate_win_probability(hole_cards, community_cards, num_opponents, num_simulations=10000):
    known_cards = hole_cards + community_cards
    full_deck = Deck()
    remaining_cards = [card for card in full_deck.cards if card not in known_cards]

    card_needed = 5 - len(community_cards)

    win = 0

    for _ in range(num_simulations):
        random.shuffle(remaining_cards)

        simulated_community = community_cards + remaining_cards[:card_needed]

        available_cards = remaining_cards[card_needed:]

        opponent_hands = []
        for i in range(num_opponents):
            opponent_hand = available_cards[i*2 : i*2 + 2]
            opponent_hands.append(opponent_hand)

        your_cards = hole_cards + simulated_community
        your_best = max(evaluate_hand(list(hand)) for hand in combinations(your_cards, 5))

        you_win = True
        for opp_hand in opponent_hands:
            opp_cards = opp_hand + simulated_community
            opp_best = max(evaluate_hand(list(hand)) for hand in combinations(opp_cards, 5))
            if opp_best >= your_best:
                you_win = False
                break

        if you_win:
            win += 1

    return win/num_simulations