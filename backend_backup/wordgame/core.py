from wordgame.utils import remover_acentos, colorir_palavra
from wordgame.palavras import carregar_palavras, validar_palavra


class Jogo:
    def __init__(self):
        self.palavras = carregar_palavras()
        self.palavra_resposta = self._escolher_palavra()
        self.palavra_resposta_normalizada = remover_acentos(self.palavra_resposta)
        self.tentativas = []

    def _escolher_palavra(self):
        import random
        return random.choice(self.palavras)

    def tentar(self, palavra: str):
        palavra_normalizada = remover_acentos(palavra)
        self.tentativas.append((palavra, palavra_normalizada))
        resultado = colorir_palavra(
            palavra, self.palavra_resposta,
            palavra_normalizada, self.palavra_resposta_normalizada
        )
        acertou = palavra_normalizada == self.palavra_resposta_normalizada
        return resultado, acertou
