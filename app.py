from flask import Flask, render_template, redirect, url_for, request
from player import Player
from game import Game

app = Flask(__name__)
app.secret_key = "poker-ai-secret-key"

game: Game = None

@app.route("/")
def index():
    return render_template('index.html', game=None)

@app.route("/start", methods=['POST'])
def start():
    global game
    num_bots = int(request.form.get("num_bots", 2))
    players = [Player("You", [], 1000)]

    for i in range (num_bots):
        players.append(Player(f"Bot{i+1}", [], 1000, is_bot=True))

    game = Game(players)
    game.start_hand()
    return redirect(url_for("play"))

@app.route("/play")
def play():
    if game is None:
        return redirect(url_for("index"))
    current_player = game.get_current_player()
    return render_template("index.html", game=game, current_player=current_player)

@app.route("/action", methods=['POST'])
def action():
    global game
    if game is None:
        return redirect(url_for("index"))
    action = request.form.get("action")
    amount = int(request.form.get("amount", 0))

    #get current player
    player = game.get_current_player()
    if player and not player.is_bot:
        game.process_action(player, action, amount)

    # process bot actions until it's human's turn or round is over
    while True:
        current = game.get_current_player()
        if current is None:
            # round is over, advance to next street
            status, message = game.advance_round()
            if status == "winner":
                return redirect(url_for("play"))

        elif current.is_bot:
            from ai import bot_action
            current_pot = game.pot + sum(p.total_bet_this_round for p in game.players)
            active_opponents = len([p for p in game.players if not p.is_folded and p != current])
            bot_act, bot_amount = bot_action(current, game.highest_bet, game.community_cards, active_opponents, current_pot)
            game.process_action(current, bot_act.lower(), bot_amount)
        else:
            # human's turn — stop and show the page
            break

    return redirect(url_for("play"))

if __name__ == '__main__':
    app.run(debug=True)