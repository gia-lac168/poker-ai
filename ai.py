from montecarlo import estimate_win_probability

def bot_action(player, highest_bet, community_cards, active_opponents):
    prob = estimate_win_probability(player.hole_cards, community_cards, active_opponents)

    if prob > 0.7:
        raise_amount = max(int(player.chips * 0.5), highest_bet + 1)
        action = ("Raise", raise_amount)
    elif prob > 0.5:
        raise_amount = max(int(player.chips * 0.25), highest_bet + 1)
        action = ("Raise", raise_amount)
    elif prob > 0.15:
        if highest_bet == 0:
            action = ("Check", 0)
        else:
            action = ("Call", 0)
    else:
        action = ("Fold", 0)

    return action
