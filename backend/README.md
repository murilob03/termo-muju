# 🟢 Word Game API

API simples para um jogo de adivinhação de palavras (estilo Wordle) feita com Flask.

## 🚀 Como usar

### 📦 Endpoint disponível

#### `POST /guess`

Envia uma tentativa de palavra para o jogo.

* **URL:** `http://localhost:5000/guess`
* **Método:** `POST`
* **Headers:**
  `Content-Type: application/json`
* **Corpo (JSON):**

```json
{
  "nome": "Joao",
  "palavra": "piano"
}
```

* **Resposta de sucesso – `200 OK`:**

```json
{
  "resultado": [
    { "letra": "p", "cor": "R" },
    { "letra": "i", "cor": "G" },
    { "letra": "a", "cor": "R" },
    { "letra": "n", "cor": "Y" },
    { "letra": "o", "cor": "G" }
  ],
  "tentativas": 1,
  "venceu": false
}
```

* **Códigos de cor (campo `cor`):**

  * `G`: letra correta e na posição certa (green)
  * `Y`: letra correta, mas na posição errada (yellow)
  * `R`: letra incorreta (red)

* **Erro – `400 Bad Request`:**

```json
{
  "error": "Você já venceu!"
}
```

Ou:

```json
{
  "error": "Palavra inválida!"
}
```

---

## ⚙️ Rodando localmente

1. Clone o repositório:

   ```bash
   git clone <url-do-repositorio>
   cd nome-do-repositorio
   ```
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicação:

   ```bash
   python app.py
   ```

A aplicação estará disponível em `http://localhost:5000`.
