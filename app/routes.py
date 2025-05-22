from flask import Blueprint, redirect, request, render_template, session, jsonify
from app.spotify import get_auth_url, get_token, get_user_profile, get_current_track
from app.genius import search_song_on_genius, extract_lyrics_from_url
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect('/login')

@main_bp.route('/login')
def login():
    auth_url = get_auth_url()
    return redirect(auth_url)

@main_bp.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Nenhum código recebido", 400

    token_data = get_token(code)
    access_token = token_data.get('access_token')

    if not access_token:
        return f"Erro ao obter token: {token_data}", 400

    session['access_token'] = access_token
    user_data = get_user_profile(access_token)

    nome = user_data.get('display_name', 'Usuário')
    email = user_data.get('email', 'não disponível')
    imagem = user_data.get('images', [{}])[0].get('url', '') if user_data.get('images') else ''
    pais = user_data.get('country', 'Desconhecido')
    produto = user_data.get('product', 'desconhecido').capitalize()
    seguidores = user_data.get('followers', {}).get('total', 0)
    perfil_url = user_data.get('external_urls', {}).get('spotify', '#')

    return render_template('index.html',
                           nome=nome,
                           email=email,
                           imagem=imagem,
                           pais=pais,
                           produto=produto,
                           seguidores=seguidores,
                           perfil_url=perfil_url,
                           track=None)


@main_bp.route('/current-track')
def current_track():
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({'error': 'Usuário não autenticado'}), 401

    track = get_current_track(access_token)
    return jsonify({'track': track})

@main_bp.route('/testar-genius')
def testar_genius():
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({'erro': 'Usuário não autenticado'}), 401

    try:
        track_str = get_current_track(access_token)
        if not track_str or "Nenhuma música" in track_str:
            return jsonify({'erro': 'Nenhuma música tocando'}), 404

        if " - " not in track_str:
            return jsonify({'erro': 'Formato da música inválido'}), 400

        partes = track_str.rsplit(" - ", 1)
        titulo = partes[0].strip()
        artista = partes[1].strip()

        url_letra = search_song_on_genius(titulo, artista)
        if not url_letra:
            return jsonify({'erro': 'Música não encontrada no Genius'}), 404

        letra = extract_lyrics_from_url(url_letra)
        if not letra:
            return jsonify({'erro': 'Não foi possível extrair a letra da música'}), 500

        return jsonify({
            "mensagem": "Letra obtida com sucesso",
            "musica": titulo,
            "artista": artista,
            "url_encontrada": url_letra,
            "letra": letra[:2000]
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@main_bp.route('/analisar-letra', methods=['POST'])
def analisar_letra():
    data = request.get_json()
    letra = data.get("letra", "")
    if not letra:
        return jsonify({'erro': 'Letra não fornecida'}), 400

    try:
        resposta = requests.post("http://127.0.0.1:5001/analisar-letra", json={"texto": letra[:2000]})
        if resposta.status_code != 200:
            return jsonify({'erro': 'Erro ao analisar letra'}), 500
        return jsonify(resposta.json())

    except Exception as e:
        return jsonify({'erro': str(e)}), 500
