from flask import Flask, request, jsonify, session, render_template
from wordgame.core import Jogo
from wordgame.palavras import validar_palavra
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend
app.secret_key = "supersecretkey"  # Needed for session

# In-memory storage for the game
jogo = {"instance": Jogo(), "created_at": datetime.now()}

# Dict to track players
players = {}


@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    name = data.get("nome")
    palavra = data.get("palavra", "").strip().lower()

    if name not in players.keys():
        players[name] = ([], False)

    if players[name][1]:
        return jsonify({"error": "Você já venceu!"}), 400

    valido, mensagem = validar_palavra(palavra)
    if not valido:
        return jsonify({"error": mensagem}), 400

    resultado, venceu = jogo["instance"].tentar(palavra)

    tentativas, _ = players[name]
    tentativas.append(palavra)
    players[name] = (tentativas, venceu)

    return jsonify(
        {"resultado": resultado, "venceu": venceu, "tentativas": len(tentativas)}
    )


if __name__ == "__main__":
    app.run(debug=True)
