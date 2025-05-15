import csv
import random
import unicodedata
import hunspell
import os
import platform


def remover_acentos(texto):
    """Remove acentos e converte para minúsculas."""
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c)
    ).lower()


def limpar_tela():
    """Limpa a tela do terminal."""
    os.system("cls" if platform.system() == "Windows" else "clear")


def colorir_palavra(palavra, resposta, palavra_normalizada, resposta_normalizada):
    """Retorna a palavra colorida para printar."""
    resultado = ["" for _ in range(5)]
    letras_restantes = list(resposta_normalizada)

    # Colore de verde as letras nas posições corretas
    for i in range(5):
        letra = palavra[i]
        letra_sem_acento = palavra_normalizada[i]

        if letra_sem_acento == resposta_normalizada[i]:
            resultado[i] = f"\033[92m{letra} \033[0m"
            letras_restantes[i] = None  # Remove a letra da lista de letras restantes

    # Colore de amarelo as letras que estão na palavra, mas em posições diferentes
    # e de vermelho as letras que não estão na palavra
    for i in range(5):
        letra = palavra[i]
        letra_sem_acento = palavra_normalizada[i]

        if letra_sem_acento != resposta_normalizada[i]:
            if letra_sem_acento in letras_restantes:
                resultado[i] = f"\033[93m{letra} \033[0m"
                letras_restantes[letras_restantes.index(letra_sem_acento)] = (
                    None  # Remove a letra da lista de letras restantes
                )
            else:
                resultado[i] = f"\033[91m{letra} \033[0m"  # Vermelho
    return "".join(resultado)


# Inicializa Hunspell
hobj = hunspell.HunSpell(
    "/usr/share/hunspell/pt_BR.dic", "/usr/share/hunspell/pt_BR.aff"
)

# Lê palavras do CSV
first_column = []
with open("filtered_words.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:
            first_column.append(row[0])

palavra_resposta = random.choice(first_column).lower()
palavra_resposta_normalizada = remover_acentos(palavra_resposta)

tentativas = []

while True:
    limpar_tela()

    # Mostra tentativas anteriores
    for tentativa, tentativa_normalizada in tentativas:
        print(
            colorir_palavra(
                tentativa,
                palavra_resposta,
                tentativa_normalizada,
                palavra_resposta_normalizada,
            )
        )

    palavra = input("\nDigite uma palavra: ").strip().lower()
    palavra_normalizada = remover_acentos(palavra)

    if len(palavra) != 5:
        print("A palavra deve ter 5 letras.")
        input("Pressione Enter para continuar...")
        continue

    # Validação com Hunspell e acento flexível
    if not hobj.spell(palavra):
        sugestoes = hobj.suggest(palavra)
        sugestoes_normalizadas = [remover_acentos(s) for s in sugestoes]
        if palavra_normalizada not in sugestoes_normalizadas:
            print("A palavra não é válida.")
            input("Pressione Enter para continuar...")
            continue

    # Adiciona à lista de tentativas
    tentativas.append((palavra, palavra_normalizada))

    # Verifica se acertou
    if palavra_normalizada == palavra_resposta_normalizada:
        limpar_tela()
        for tentativa, tentativa_normalizada in tentativas:
            print(
                colorir_palavra(
                    tentativa,
                    palavra_resposta,
                    tentativa_normalizada,
                    palavra_resposta_normalizada,
                )
            )
        print("\n\033[92mVocê acertou!\033[0m")
        break
