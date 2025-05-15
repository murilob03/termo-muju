import csv
import hunspell
from wordgame.utils import remover_acentos

# Inicializa Hunspell uma única vez
_hunspell = hunspell.HunSpell("/usr/share/hunspell/pt_BR.dic", "/usr/share/hunspell/pt_BR.aff")


def carregar_palavras():
    with open("word_list.csv", newline="", encoding="utf-8") as csvfile:
        return [row[0].strip().lower() for row in csv.reader(csvfile) if row]


def validar_palavra(palavra: str):
    if len(palavra) != 5:
        return False, "A palavra deve ter 5 letras."

    if not _hunspell.spell(palavra):
        sugestoes = _hunspell.suggest(palavra)
        normalizadas = [remover_acentos(s) for s in sugestoes]
        if remover_acentos(palavra) not in normalizadas:
            return False, "A palavra não é válida."

    return True, ""
