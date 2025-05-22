# 🎧 Emotionfy – Música, Emoção e Inteligência Artificial

O **Emotionfy** é uma aplicação web que une **Spotify**, **Genius** e **OpenAI** para analisar letras de músicas, identificar emoções e **gerar imagens com inteligência artificial** que representam visualmente essas emoções.

<img src="https://i.postimg.cc/nz29qyPG/emotionfy.png" alt="Emotionfy Banner" width="100" height="100" />

---

## ✨ Funcionalidades

- 🔐 Login com sua conta Spotify via OAuth 2.0
- 🎵 Identificação da música que você está ouvindo no momento
- 📜 Busca automática da letra da música via Genius API
- 🧠 Análise emocional da letra com OpenAI GPT-4
- 🎨 Geração de imagem com DALL·E baseada na emoção detectada
- ⬇️ Opção para baixar a imagem gerada
- 🌙 Interface escura, responsiva e intuitiva

---

## 🛠️ Tecnologias Utilizadas

| Camada        | Tecnologia                                                                 |
|---------------|----------------------------------------------------------------------------|
| Backend       | [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/) |
| Frontend      | HTML, CSS (custom), JS Vanilla                                             |
| Autenticação  | [Spotify OAuth 2.0](https://developer.spotify.com/documentation/general/guides/authorization/) |
| APIs          | [Spotify Web API](https://developer.spotify.com/documentation/web-api/), [Genius API](https://docs.genius.com/), [OpenAI GPT-4 + DALL·E](https://platform.openai.com/) |
| IA e Geração  | [OpenAI GPT-4](https://openai.com/gpt-4), [DALL·E](https://openai.com/dall-e) |
| Hospedagem    | Localhost (modo dev)                                                       |

---

## 🧪 Como Rodar Localmente

### Pré-requisitos

- Python 3.10+
- Conta Spotify com acesso a Developer Dashboard
- Conta OpenAI com créditos ativos
- Genius API Key

### Instalação

```bash
git clone https://github.com/seunome/emotionfy.git
cd emotionfy
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
pip install -r requirements.txt
Configuração
Crie um arquivo .env com as variáveis:

env

SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
GENIUS_API_KEY=your_genius_key
OPENAI_API_KEY=your_openai_key
Executar
bash

python app.py
# ou com Flask:
flask run
Acesse: http://localhost:5000
