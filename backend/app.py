from flask import Flask, request, jsonify, session
from wordgame.core import Jogo
from wordgame.palavras import validar_palavra
from flask_cors import CORS
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from contextlib import contextmanager

from models import SessionLocal, HistoricoPartida

MAXIMO_TENTATIVAS = 5


def check_reset_jogo():
    """Troca a palavra nas horas múltiplas de 5 e salva resultados dos jogadores."""
    now = datetime.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    if (
        now.hour % 5 == 0
        and jogo["created_at"].replace(minute=0, second=0, microsecond=0)
        != current_hour
    ):
        # Salva resultados no bd
        for nome, (tentativas, venceu) in players.items():
            salvar_partida(nome, tentativas, venceu)

        # Reseta o jogo
        jogo["instance"] = Jogo()
        jogo["created_at"] = now
        players.clear()


# Cria e inicia o agendador
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_reset_jogo, trigger="interval", minutes=1)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def salvar_partida(nome, tentativas, venceu):
    with get_db() as db:
        partida = HistoricoPartida(
            nome=nome,
            tentativas=len(tentativas),
            venceu=venceu,
            jogada_em=datetime.now(),
        )
        db.add(partida)
        db.commit()


app = Flask(__name__)
CORS(app)
app.secret_key = "supersecretkey"

# Game state
jogo = {"instance": Jogo(), "created_at": datetime.now()}

players = {}
historico = []  # ← Armazena histórico de partidas


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"mensagem": "OK"})


@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    nome = data.get("nome")
    palavra = data.get("palavra", "").strip().lower()

    if nome not in players:
        players[nome] = ([], False)

    if players[nome][1]:
        return jsonify({"error": "Você já venceu esta rodada!"}), 400
    if len(players[nome][0]) >= MAXIMO_TENTATIVAS:
        return jsonify({"error": "Você atingiu o número máximo de tentativas!"}), 400

    valido, mensagem = validar_palavra(palavra)
    if not valido:
        return jsonify({"error": mensagem}), 400

    resultado, venceu = jogo["instance"].tentar(palavra)

    tentativas, _ = players[nome]
    tentativas.append(palavra)
    players[nome] = (tentativas, venceu)

    if players[nome][1] or len(players[nome][0]) >= MAXIMO_TENTATIVAS:
        salvar_partida(nome, tentativas, venceu)

    return jsonify(
        {"resultado": resultado, "venceu": venceu, "tentativas": len(tentativas)}
    )


@app.route("/historico", methods=["GET"])
def get_historico():
    with get_db() as db:
        resultados = (
            db.query(HistoricoPartida).order_by(HistoricoPartida.jogada_em.desc()).all()
        )

    return jsonify(
        [
            {
                "nome": r.nome,
                "tentativas": r.tentativas,
                "venceu": r.venceu,
                "jogada_em": r.jogada_em.strftime("%Y-%m-%d %H:%M"),
            }
            for r in resultados
        ]
    )


if __name__ == "__main__":
    app.run(debug=True)
