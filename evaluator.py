from collections import Counter

def evaluate_hand(cards):
    ranks = [card.rank for card in cards]
    ranks_count = Counter(ranks)

    counts = sorted(ranks_count.values(), reverse=True)
    if counts == [4, 1]:
        return 8
    elif counts == [3, 2]:
        return 7
    elif counts == [3, 1, 1]:
        return 4
    elif counts == [2, 2, 1]:
        return 3
    elif counts == [2, 1, 1, 1]:
        return 2
    elif counts == [1, 1, 1, 1, 1]:
        return 1
