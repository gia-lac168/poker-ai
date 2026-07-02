from deck import Card
from evaluator import evaluate_hand

test_hands = [
    ([Card("10","♠"), Card("J","♠"), Card("Q","♠"), Card("K","♠"), Card("A","♠")], (10,), "Royal Flush"),
    ([Card("5","♠"), Card("6","♠"), Card("7","♠"), Card("8","♠"), Card("9","♠")], (9, 9), "Straight Flush"),
    ([Card("4","♠"), Card("4","♥"), Card("4","♦"), Card("4","♣"), Card("K","♠")], (8, 4, 13), "Four of a Kind"),
    ([Card("4","♠"), Card("4","♥"), Card("4","♦"), Card("K","♣"), Card("K","♠")], (7, 4, 13), "Full House"),
    ([Card("2","♠"), Card("7","♠"), Card("9","♠"), Card("J","♠"), Card("K","♠")], (6, 13, 11, 9, 7, 2), "Flush"),
    ([Card("5","♠"), Card("6","♥"), Card("7","♦"), Card("8","♣"), Card("9","♠")], (5, 9), "Straight"),
    ([Card("4","♠"), Card("4","♥"), Card("4","♦"), Card("9","♣"), Card("K","♠")], (4, 4, 13, 9), "Three of a Kind"),
    ([Card("4","♠"), Card("4","♥"), Card("K","♦"), Card("K","♣"), Card("2","♠")], (3, 13, 4, 2), "Two Pair"),
    ([Card("4","♠"), Card("4","♥"), Card("9","♦"), Card("J","♣"), Card("K","♠")], (2, 4, 13, 11, 9), "One Pair"),
    ([Card("2","♠"), Card("7","♥"), Card("9","♦"), Card("J","♣"), Card("K","♠")], (1, 13, 11, 9, 7, 2), "High Card"),
]

for hand, expected, name in test_hands:
    result = evaluate_hand(hand)
    status = "✅" if result == expected else "❌"
    print(f"{status} {name}: expected {expected}, got {result}")