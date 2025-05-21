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
    print(f"Texto recebido para análise: {texto[:200]}...")

    prompt = f"""
Analise a emoção predominante da seguinte letra de música e retorne **exatamente** no seguinte formato:

Emoção: <uma palavra>
Cores: <cor1>, <cor2>, <cor3>
Descrição: <até 20 palavras>
Tema: <tema principal da música em uma frase>
Tom Narrativo: <ponto de vista ou estilo de narração (ex: 1ª pessoa, introspectivo)>
Mensagem Central: <intenção principal do artista em até 20 palavras>
Dispositivos Estilísticos: <exemplos de figuras de linguagem ou estilos usados>
Palavras-chave: <lista de até 5 palavras marcantes da letra>

Letra:
{texto}
"""

    try:
        print("Enviando requisição para a OpenAI...")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente inteligente que analisa letras de música."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )

        content = response.choices[0].message.content
        print("Resposta crua da OpenAI:")
        print(repr(content))  # Para debug, mostra quebras de linha etc.

        # Regex para extrair todos os campos
        regex = re.compile(
            r"Emoção:\s*(?P<emocao>.+?)\s*[\r\n]+"
            r"Cores:\s*(?P<cores>.+?)\s*[\r\n]+"
            r"Descrição:\s*(?P<descricao>.+?)\s*[\r\n]+"
            r"Tema:\s*(?P<tema>.+?)\s*[\r\n]+"
            r"Tom Narrativo:\s*(?P<tom>.+?)\s*[\r\n]+"
            r"Mensagem Central:\s*(?P<mensagem>.+?)\s*[\r\n]+"
            r"Dispositivos Estilísticos:\s*(?P<estilo>.+?)\s*[\r\n]+"
            r"Palavras-chave:\s*(?P<palavras>.+)",
            re.IGNORECASE | re.DOTALL
        )

        match = regex.search(content)
        if not match:
            raise ValueError("Resposta inesperada do modelo.")

        # Extrair e preparar os dados
        emocao = match.group("emocao").strip()
        cores = [cor.strip() for cor in match.group("cores").split(",")]
        descricao = match.group("descricao").strip()
        tema = match.group("tema").strip()
        tom = match.group("tom").strip()
        mensagem = match.group("mensagem").strip()
        estilo = match.group("estilo").strip()
        palavras = [p.strip() for p in match.group("palavras").split(",")]

        return jsonify({
            "emocao": emocao,
            "cores": cores,
            "descricao": descricao,
            "tema": tema,
            "tom_narrativo": tom,
            "mensagem_central": mensagem,
            "dispositivos_estilisticos": estilo,
            "palavras_chave": palavras
        })

    except Exception as e:
        print(f"Erro ao processar: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
