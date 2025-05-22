from openai import OpenAI
import os
import re
import requests
from io import BytesIO
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ultima_analise = None
ultima_imagem_url = None

@app.route("/analisar-letra", methods=["POST"])
def analisar_letra():
    data = request.get_json()

    if not data or not data.get("texto"):
        return jsonify({"error": "Campo 'texto' é obrigatório."}), 400

    texto = data["texto"]

    prompt_analise = f"""
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente inteligente que analisa letras de música."},
                {"role": "user", "content": prompt_analise}
            ],
            max_tokens=400,
            temperature=0.7
        )

        content = response.choices[0].message.content

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

        resultado = {
            "emocao": match.group("emocao").strip(),
            "cores": [c.strip() for c in match.group("cores").split(",")],
            "descricao": match.group("descricao").strip(),
            "tema": match.group("tema").strip(),
            "tom_narrativo": match.group("tom").strip(),
            "mensagem_central": match.group("mensagem").strip(),
            "dispositivos_estilisticos": match.group("estilo").strip(),
            "palavras_chave": [p.strip() for p in match.group("palavras").split(",")]
        }

        global ultima_analise
        ultima_analise = resultado

        return jsonify(resultado)

    except Exception as e:
        print(f"Erro ao processar: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/gerar-imagem", methods=["POST"])
def gerar_imagem():
    global ultima_analise, ultima_imagem_url

    if not ultima_analise:
        return jsonify({"error": "Nenhuma análise disponível para gerar imagem."}), 400

    prompt_dinamico = (
        f"Uma cena artística que represente a emoção '{ultima_analise['emocao']}', "
        f"com o tema '{ultima_analise['tema']}'. "
        f"Transmita visualmente a seguinte descrição: '{ultima_analise['descricao']}'. "
        f"Use um estilo {ultima_analise['tom_narrativo'].lower()}, "
        f"com elementos que comuniquem: '{ultima_analise['mensagem_central']}'. "
        f"Incorpore cores como: {', '.join(ultima_analise['cores'])}. "
        f"Inspiração visual: {', '.join(ultima_analise['palavras_chave'])}."
    )

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_dinamico,
            size="1024x1024",
            n=1
        )
        url_imagem = response.data[0].url
        ultima_imagem_url = url_imagem

        return jsonify({
            "prompt_usado": prompt_dinamico,
            "url": url_imagem
        })
    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")
        return jsonify({"error": "Erro ao gerar imagem"}), 500

@app.route("/download-imagem", methods=["GET"])
def download_imagem():
    global ultima_imagem_url

    if not ultima_imagem_url:
        return jsonify({"error": "Nenhuma imagem disponível para download."}), 400

    try:
        response = requests.get(ultima_imagem_url)
        response.raise_for_status()

        return send_file(
            BytesIO(response.content),
            mimetype="image/png",
            as_attachment=True,
            download_name="imagem_gerada.png"
        )
    except Exception as e:
        print(f"Erro ao baixar imagem: {e}")
        return jsonify({"error": "Erro ao baixar imagem para download."}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
