from openai import OpenAI
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Instancia o client da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/analisar-letra", methods=["POST"])
def analisar_letra():
    data = request.get_json()

    if not data or not data.get("texto"):
        return jsonify({"error": "Campo 'texto' é obrigatório."}), 400

    texto = data["texto"]
    print(f"Texto recebido para análise: {texto}")

    prompt = f"""
Analise a emoção predominante da seguinte letra de música e retorne no seguinte formato exato:

Emoção: <uma palavra>
Cores: <cor1>, <cor2>, <cor3>
Descrição: <até 20 palavras>

Letra:
{texto}
"""

    try:
        print("Enviando requisição para a OpenAI...")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente inteligente."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        content = response.choices[0].message.content
        print("Resposta crua da OpenAI:")
        print(repr(content))  # Mostra quebras de linha, espaços etc.

        # Regex pra pegar os campos esperados
        match = re.search(
            r"Emoção:\s*(?P<emocao>\w+)\s*[\r\n]+"
            r"Cores:\s*(?P<cores>[^,\n]+,\s*[^,\n]+,\s*[^,\n]+)\s*[\r\n]+"
            r"Descrição:\s*(?P<descricao>.+)",
            content,
            re.IGNORECASE
        )

        if not match:
            raise ValueError("Resposta inesperada do modelo.")

        emocao = match.group("emocao").strip()
        cores = [cor.strip() for cor in match.group("cores").split(",")]
        descricao = match.group("descricao").strip()

        return jsonify({
            "emocao": emocao,
            "cores": cores,
            "descricao": descricao
        })

    except Exception as e:
        print(f"Erro ao processar: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
