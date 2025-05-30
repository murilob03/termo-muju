from flask import Flask, request, jsonify, session
from wordgame.core import Jogo
from wordgame.palavras import validar_palavra
from flask_cors import CORS
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit


def check_reset_jogo():
    """Troca a palavra nas horas múltiplas de 5 e salva resultados dos jogadores."""
    now = datetime.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    if (
        now.hour % 5 == 0
        and jogo["created_at"].replace(minute=0, second=0, microsecond=0)
        != current_hour
    ):
        # Salva resultados antes de resetar
        for nome, (tentativas, venceu) in players.items():
            historico.append(
                {
                    "nome": nome,
                    "tentativas": tentativas,
                    "venceu": venceu,
                    "jogada_em": jogo["created_at"].strftime("%Y-%m-%d %H:%M"),
                }
            )

        # Reseta o jogo
        jogo["instance"] = Jogo()
        jogo["created_at"] = now
        players.clear()


# Cria e inicia o agendador
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_reset_jogo, trigger="interval", minutes=1)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

app = Flask(__name__)
CORS(app)
app.secret_key = "supersecretkey"

# Game state
jogo = {"instance": Jogo(), "created_at": datetime.now()}

players = {}
historico = []  # ← Armazena histórico de partidas


@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    name = data.get("nome")
    palavra = data.get("palavra", "").strip().lower()

    if name not in players:
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


@app.route("/historico", methods=["GET"])
def get_historico():
    """Retorna histórico de jogos anteriores (não persistente)."""
    return jsonify(historico)


if __name__ == "__main__":
    app.run(debug=True)
