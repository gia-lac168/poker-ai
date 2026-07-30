from montecarlo import estimate_win_probability

def bot_action(player, highest_bet, community_cards, active_opponents, pot):

    prob = estimate_win_probability(player.hole_cards, community_cards, active_opponents, num_simulations=2000)

    amount_to_call = highest_bet - player.total_bet_this_round
    if amount_to_call > 0:
        pot_odds = amount_to_call / (pot + amount_to_call)
    else:
        pot_odds = 0

    if prob > 0.65:
        raise_amount = int(pot * 0.75)
        raise_amount = max(raise_amount, highest_bet + 1)
        raise_amount = min(raise_amount, player.chips + player.total_bet_this_round)
        if raise_amount <= highest_bet:
            action = ("Call", 0, f"Win prob: {prob:.1%} | Pot odds: {pot_odds:.1%} | Strong hand but can't raise — calling")
        else:
            action = ("Raise", raise_amount, f"Win prob: {prob:.1%} | Pot odds: {pot_odds:.1%} | Strong hand (>65%) — raised 75% of pot")

    elif prob > pot_odds:
        if prob >= 0.60:
            raise_amount = int(pot * 0.5)
            raise_amount = max(raise_amount, highest_bet + 1)
            raise_amount = min(raise_amount, player.chips + player.total_bet_this_round)
            if raise_amount <= highest_bet:
                action = ("Call", 0, f"Win prob: {prob:.1%} | Pot odds: {pot_odds:.1%} | Decent hand but can't raise — calling")
            else:
                action = ("Raise", raise_amount, f"Win prob: {prob:.1%} | Pot odds: {pot_odds:.1%} | Decent hand (>60%) — raised 50% of pot")
        elif prob >= 0.35:
            if highest_bet == 0:
                action = ("Check", 0, f"Win prob: {prob:.1%} | Free check — marginal hand")
            else:
                action = ("Call", 0, f"Win prob: {prob:.1%} | Pot odds: {pot_odds:.1%} | Marginal but profitable — calling")
        else:
            if highest_bet == 0:
                action = ("Check", 0, f"Win prob: {prob:.1%} | Free check — weak hand")
            else:
                action = ("Fold", 0, f"Win prob: {prob:.1%} | Pot odds: {pot_odds:.1%} | Too weak despite pot odds — folding")

    else:
        action = ("Fold", 0, f"Win prob: {prob:.1%} | Pot odds: {pot_odds:.1%} | Unprofitable to call — folding")

    return action
