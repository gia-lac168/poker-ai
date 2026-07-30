from flask import Flask, render_template, redirect, url_for, request
from player import Player
from game import Game

app = Flask(__name__)
app.secret_key = "poker-ai-secret-key"

game: Game = None
action_log = []
winner_message = None

stats = {
    "hands_played": 0,
    "hands_won": 0,
    "biggest_pot": 0,
    "chip_history": [1000]
}

@app.route("/")
def index():
    return render_template('index.html', game=None, stats=stats)

@app.route("/start", methods=['POST'])
def start():
    global game, action_log, winner_message, stats

    # update stats from previous hand if exists
    if game is not None:
        stats["hands_played"] += 1
        you = next(p for p in game.players if not p.is_bot)
        stats["chip_history"].append(you.chips)
        if winner_message and "You" in winner_message:
            stats["hands_won"] += 1
            if game.last_pot > stats["biggest_pot"]:
                stats["biggest_pot"] = game.last_pot

        # keep existing players and their chips!
        existing_chips = {p.name: p.chips for p in game.players}
        num_bots = len([p for p in game.players if p.is_bot])

        def get_chips(name):
            chips = existing_chips.get(name, 1000)
            return 1000 if chips <= 0 else chips  # rebuy if broke

        players = [Player("You", [], get_chips("You"))]
        for i in range(num_bots):
            name = f"Bot{i + 1}"
            players.append(Player(name, [], get_chips(name), is_bot=True))
    else:
        num_bots = int(request.form.get("num_bots", 2))
        players = [Player("You", [], 1000)]
        for i in range(num_bots):
            players.append(Player(f"Bot{i + 1}", [], 1000, is_bot=True))

    action_log = []
    winner_message = None
    game = Game(players)
    game.start_hand()
    return redirect(url_for("play"))

@app.route("/play")
def play():
    if game is None:
        return redirect(url_for("index"))
    current_player = game.get_current_player()
    win_prob = None
    round_names = {0: "Pre-flop", 1: "Flop", 2: "Turn", 3: "River", 4: "Showdown"}
    current_round_name = round_names.get(game.current_round, "Pre-flop")
    if current_player and not current_player.is_bot:
        from montecarlo import estimate_win_probability
        active_opponents = len([p for p in game.players if not p.is_folded and p != current_player])
        win_prob = f"{estimate_win_probability(current_player.hole_cards, game.community_cards, active_opponents, num_simulations=2000):.1%}"
    return render_template("index.html", game=game, current_player=current_player, win_prob=win_prob,
                           current_round_name=current_round_name, action_log=action_log, winner_message=winner_message,
                           game_over=game.game_over, stats=stats)

@app.route("/action", methods=['POST'])
def action():
    global game, action_log, winner_message
    if game is None:
        return redirect(url_for("index"))
    player_action = request.form.get("action")
    amount_str = request.form.get("amount", "0")
    amount = int(amount_str) if amount_str.strip() else 0

    if player_action == "raise" and amount <= game.highest_bet:
        player_action = "call"  # fallback if raise amount invalid

    #get current player
    player = game.get_current_player()
    if player and not player.is_bot:
        msg = game.process_action(player, player_action, amount)
        action_log.append(msg)

    # process bot actions until it's human's turn or round is over
    while True:
        current = game.get_current_player()
        if current is None:
            # round is over, advance to next street
            status, message = game.advance_round()
            action_log.append(message)
            if status == "winner":
                winner_message = message
                return redirect(url_for("play"))
            elif status == "continue":
                active_can_act = [p for p in game.players if not p.is_folded and not p.is_all_in]
                if len(active_can_act) == 0:
                    continue  # everyone all-in, keep advancing
                else:
                    break  # someone can act, stop

        elif current.is_bot:
            from ai import bot_action
            current_pot = game.pot + sum(p.total_bet_this_round for p in game.players)
            active_opponents = len([p for p in game.players if not p.is_folded and p != current])
            bot_act, bot_amount, bot_reasoning = bot_action(current, game.highest_bet, game.community_cards, active_opponents, current_pot)
            msg = game.process_action(current, bot_act.lower(), bot_amount)
            action_log.append(f"{msg} → {bot_reasoning}")
        else:
            # human's turn — stop and show the page
            break

    return redirect(url_for("play"))

@app.route("/advance", methods=['POST']) #for bots' action when player folded
def advance():
    global game, action_log, winner_message
    if game is None:
        return redirect(url_for("index"))

    while True:
        current = game.get_current_player()
        if current is None:
            status, message = game.advance_round()
            action_log.append(message)
            if status == "winner":
                winner_message = message
                break
            active_can_act = [p for p in game.players if not p.is_folded and not p.is_all_in]
            if len(active_can_act) == 0:
                continue
            else:
                break
        elif current.is_bot:
            from ai import bot_action
            current_pot = game.pot + sum(p.total_bet_this_round for p in game.players)
            active_opponents = len([p for p in game.players if not p.is_folded and p != current])
            bot_act, bot_amount, bot_reasoning = bot_action(current, game.highest_bet, game.community_cards, active_opponents, current_pot)
            msg = game.process_action(current, bot_act.lower(), bot_amount)
            action_log.append(f"{msg} → {bot_reasoning}")
        else:
            break

    return "", 204  # return empty response

if __name__ == '__main__':
    app.run(debug=True)