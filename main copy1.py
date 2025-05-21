from openai import OpenAI
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Instanciar o client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/analisar-letra", methods=["POST"])
def analisar_letra():
    data = request.get_json()

    if not data or not data.get("texto"):
        return jsonify({"error": "Campo 'texto' é obrigatório."}), 400

    texto = data["texto"]
    print(f"Texto recebido para análise: {texto}")

    prompt = f"""
    Analise a emoção predominante da seguinte letra de música e retorne:
    1. Emoção dominante (uma palavra)
    2. Paleta de 3 cores hexadecimais que representam a emoção
    3. Uma breve descrição da vibe da música (até 20 palavras)

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

        content = response.choices[0].message.content.strip()
        print("Conteúdo extraído:")
        print(content)

        linhas = content.splitlines()
        return jsonify({
            "emocao": linhas[0].split(":")[-1].strip(),
            "cores": [cor.strip() for cor in linhas[1].split(":")[-1].split(",")],
            "descricao": linhas[2].split(":")[-1].strip()
        })

    except Exception as e:
        print(f"Erro ao processar: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
