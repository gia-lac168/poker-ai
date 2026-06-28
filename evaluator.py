from collections import Counter

def evaluate_hand(cards):
    ranks = [card.rank for card in cards]
    ranks_count = Counter(ranks)

    counts = sorted(ranks_count.values(), reverse=True)
    if is_royal_flush(cards):
        return 10
    elif is_straight_flush(cards):
        return 9
    elif counts == [4, 1]:
        return 8
    elif counts == [3, 2]:
        return 7
    elif is_flush(cards):
        return 6
    elif is_straight(cards):
        return 5
    elif counts == [3, 1, 1]:
        return 4
    elif counts == [2, 2, 1]:
        return 3
    elif counts == [2, 1, 1, 1]:
        return 2
    elif counts == [1, 1, 1, 1, 1]:
        return 1

def is_flush(cards):
    suits = [card.suit for card in cards]
    return len(set(suits)) == 1

def is_straight(cards):
    rank_values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13, "A":14}
    ranks = sorted(set(rank_values[card.rank] for card in cards))

    if set(ranks) == {14, 2, 3, 4, 5}:
        return True

    if len(set(ranks)) != 5:
        return False

    return ranks[-1] - ranks[0] == 4

def is_straight_flush(cards):
    return is_flush(cards) and is_straight(cards)

def is_royal_flush(cards):
    rank_values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13, "A":14}
    hand = set(rank_values[card.rank] for card in cards)
    return is_flush(cards) and hand == {10, 11, 12, 13, 14}