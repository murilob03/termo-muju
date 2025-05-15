from flask import Flask, request, jsonify, session
from wordgame.core import Jogo
from wordgame.palavras import validar_palavra
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend
app.secret_key = "supersecretkey"  # Needed for session

# Store games in memory (for demo; use a DB or Redis in prod)
games = {}


@app.route("/start", methods=["POST"])
def start_game():
    game_id = str(uuid.uuid4())
    game = Jogo()
    games[game_id] = game
    return jsonify({"game_id": game_id})


@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    game_id = data.get("game_id")
    palavra = data.get("palavra", "").strip().lower()

    if not game_id or game_id not in games:
        return jsonify({"error": "Invalid or missing game ID"}), 400

    valido, mensagem = validar_palavra(palavra)
    if not valido:
        return jsonify({"error": mensagem}), 400

    game = games[game_id]
    resultado, venceu = game.tentar(palavra)

    if game.venceu:
        del games[game_id]

    return jsonify(
        {"resultado": resultado, "venceu": venceu, "tentativas": len(game.tentativas)}
    )


if __name__ == "__main__":
    app.run(debug=True)
