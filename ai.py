from montecarlo import estimate_win_probability

def bot_action(player, highest_bet, community_cards, active_opponents, pot):

    prob = estimate_win_probability(player.hole_cards, community_cards, active_opponents)

    amount_to_call = highest_bet - player.total_bet_this_round
    if amount_to_call > 0:
        pot_odds = amount_to_call / (pot + amount_to_call)
    else:
        pot_odds = 0  # free check, no pot odds needed

    if prob > 0.7:
        raise_amount = min(int(pot * 0.75), player.chips + player.total_bet_this_round)
        raise_amount = max(raise_amount, highest_bet + 1)
        if raise_amount <= highest_bet:  # if it can't raise meaningfully, just call
            action = ("Call", 0)
        else:
            action = ("Raise", raise_amount)
    elif prob > pot_odds:
        if prob >= 0.5:
            raise_amount = min(int(pot * 0.5), player.chips + player.total_bet_this_round)
            raise_amount = max(raise_amount, highest_bet + 1)
            if raise_amount <= highest_bet:  # can't raise meaningfully, just call
                action = ("Call", 0)
            else:
                action = ("Raise", raise_amount)
        else:
            action = ("Check", 0) if highest_bet == 0 else ("Call", 0)
    else:
        action = ("Fold", 0)

    return action
