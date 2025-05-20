import unicodedata


def remover_acentos(texto):
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    ).lower()


def colorir_palavra(palavra, resposta, palavra_normalizada, resposta_normalizada):
    resultado = ["" for _ in range(5)]
    letras_restantes = list(resposta_normalizada)

    for i in range(5):
        letra = palavra[i]
        letra_sem_acento = palavra_normalizada[i]

        if letra_sem_acento == resposta_normalizada[i]:
            resultado[i] = {"letra": letra, "cor": "G"}
            letras_restantes[i] = None

    for i in range(5):
        letra = palavra[i]
        letra_sem_acento = palavra_normalizada[i]

        if letra_sem_acento != resposta_normalizada[i]:
            if letra_sem_acento in letras_restantes:
                resultado[i] = {"letra": letra, "cor": "Y"}
                letras_restantes[letras_restantes.index(letra_sem_acento)] = None
            else:
                resultado[i] = {"letra": letra, "cor": "R"}
    return resultado
