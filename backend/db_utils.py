from sqlalchemy import text
from models import HistoricoPartida
from datetime import timedelta


def criar_view_estatisticas(session):
    session.execute(
        text(
            """
        CREATE VIEW IF NOT EXISTS estatisticas_jogador AS
        SELECT
            nome,
            COUNT(*) AS total_partidas,
            SUM(CASE WHEN venceu = 1 THEN 1 ELSE 0 END) AS total_vitorias,
            ROUND(100.0 * SUM(CASE WHEN venceu = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS taxa_vitoria
        FROM historico_partidas
        GROUP BY nome
    """
        )
    )
    session.commit()


def calcular_streak(nome, session):
    partidas = (
        session.query(HistoricoPartida)
        .filter_by(nome=nome, venceu=True)
        .order_by(HistoricoPartida.jogada_em.asc())
        .all()
    )

    if not partidas:
        return 0

    streak = 1
    max_streak = 1

    for i in range(1, len(partidas)):
        diff = (partidas[i].jogada_em.date() - partidas[i - 1].jogada_em.date()).days
        if diff == 1:
            streak += 1
            max_streak = max(max_streak, streak)
        elif diff > 1:
            streak = 1

    return max_streak
