import os
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class HistoricoPartida(Base):
    __tablename__ = "historico_partidas"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    tentativas = Column(Integer, nullable=False)
    venceu = Column(Boolean, nullable=False)
    jogada_em = Column(DateTime, default=datetime.utcnow)


# Caminho absoluto da pasta onde está este arquivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "jogo.db")

# Cria o engine com caminho absoluto
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
