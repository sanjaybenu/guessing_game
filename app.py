from flask import Flask, request, jsonify, session, render_template
from game import Game

app = Flask(__name__)
game = None
secret_key = 'your_secret_key_here'
app.secret_key = secret_key
@app.route("/", methods=["GET" , "POST"])
def set_name():
    # ---- GET request (when the browser loads the page) ---- #
    if request.method == 'GET':
        return render_template('app.html')  # <-- your HTML file
    global game
    data = request.json
    name = data.get("name").title()
    session['name'] = name
    if not name:
        return jsonify({"error": "Name required"}), 400
    game = Game(name)
    return jsonify({"message": f"Welcome {name}!"})

@app.route("/diff_lvl", methods=["POST"])
def set_difficulty():
    global game
    data = request.json
    diff_lvl = data.get("difficulty")
    if not game:
        return jsonify({"error": "Game not initialized"}), 400
    return jsonify(game.start_game(diff_lvl))

@app.route("/game", methods=["POST"])
def play_game():
    global game
    data = request.json
    guess = data.get("guess")
    if guess is None:
        return jsonify({"error": "Guess required"}), 400
    return jsonify(game.make_guess(int(guess)))

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    global game
    if not game:
        return jsonify({"error": "Game not initialized"}), 400
    return jsonify(game.show_all_leaderboards())



@app.route("/exit", methods=["POST"])
def exit_game():
    global game
    player = session.get("name")
    return jsonify({
        "message": f"Best attempt: {game.best_score if game and game.best_score else 'No successful attempts'}",
        "leaderboards": game.
        show_all_leaderboards() if game else {},
        "player": player
    })

if __name__ == '__main__':
    app.run(debug=True)