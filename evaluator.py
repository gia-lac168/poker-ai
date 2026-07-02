from collections import Counter

RANK_VALUES = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13, "A":14}

def evaluate_hand(cards):
    ranks = [card.rank for card in cards]
    ranks_count = Counter(ranks)
    counts = sorted(ranks_count.values(), reverse=True)

    if is_royal_flush(cards):
        return (10,)

    elif is_straight_flush(cards):
        high_card = max(RANK_VALUES[card.rank] for card in cards)
        return (9, high_card)

    elif counts == [4, 1]:
        four_rank = max(RANK_VALUES[rank] for rank, count in ranks_count.items() if count == 4)
        kicker = max(RANK_VALUES[rank] for rank, count in ranks_count.items() if count == 1)
        return (8, four_rank, kicker)

    elif counts == [3, 2]:
        three_rank = max(RANK_VALUES[rank] for rank, count in ranks_count.items() if count == 3)
        pair_rank = max(RANK_VALUES[rank] for rank, count in ranks_count.items() if count == 2)
        return (7, three_rank, pair_rank)

    elif is_flush(cards):
        all_ranks = sorted([RANK_VALUES[card.rank] for card in cards], reverse=True)
        return (6, all_ranks[0], all_ranks[1], all_ranks[2], all_ranks[3], all_ranks[4])

    elif is_straight(cards):
        high_card = max(RANK_VALUES[card.rank] for card in cards)
        # handle wheel (A-2-3-4-5) — high card is 5, not Ace
        if set(RANK_VALUES[card.rank] for card in cards) == {14, 2, 3, 4, 5}:
            high_card = 5
        return (5, high_card)

    elif counts == [3, 1, 1]:
        three_rank = max(RANK_VALUES[rank] for rank, count in ranks_count.items() if count == 3)
        kickers = sorted([RANK_VALUES[rank] for rank, count in ranks_count.items() if count == 1], reverse=True)
        return (4, three_rank, kickers[0], kickers[1])

    elif counts == [2, 2, 1]:
        pairs = sorted([RANK_VALUES[rank] for rank, count in ranks_count.items() if count == 2], reverse=True)
        kicker = max(RANK_VALUES[rank] for rank, count in ranks_count.items() if count == 1)
        return (3, pairs[0], pairs[1], kicker)

    elif counts == [2, 1, 1, 1]:
        pair_rank = max(RANK_VALUES[rank] for rank, count in ranks_count.items() if count == 2)
        kickers = sorted([RANK_VALUES[rank] for rank, count in ranks_count.items() if count == 1], reverse=True)
        return (2, pair_rank, kickers[0], kickers[1], kickers[2])

    elif counts == [1, 1, 1, 1, 1]:
        all_ranks = sorted([RANK_VALUES[card.rank] for card in cards], reverse=True)
        return (1, all_ranks[0], all_ranks[1], all_ranks[2], all_ranks[3], all_ranks[4])

def is_flush(cards):
    suits = [card.suit for card in cards]
    return len(set(suits)) == 1

def is_straight(cards):
    #rank_values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13, "A":14}
    ranks = sorted(set(RANK_VALUES[card.rank] for card in cards))

    if set(ranks) == {14, 2, 3, 4, 5}:
        return True

    if len(set(ranks)) != 5:
        return False

    return ranks[-1] - ranks[0] == 4

def is_straight_flush(cards):
    return is_flush(cards) and is_straight(cards)

def is_royal_flush(cards):
    #rank_values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13, "A":14}
    hand = set(RANK_VALUES[card.rank] for card in cards)
    return is_flush(cards) and hand == {10, 11, 12, 13, 14}