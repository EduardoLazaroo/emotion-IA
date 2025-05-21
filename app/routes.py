from flask import Blueprint, redirect, request, render_template, session, jsonify
from app.spotify import get_auth_url, get_token, get_user_profile, get_current_track

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

    return render_template('index.html', nome=nome, email=email, track=None)

@main_bp.route('/current-track')
def current_track():
    access_token = session.get('access_token')
    if not access_token:
        return jsonify({'track': 'Usuário não autenticado'}), 401

    track = get_current_track(access_token)
    return jsonify({'track': track})
