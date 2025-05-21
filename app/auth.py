from flask import Blueprint, redirect, url_for, session, request
from . import oauth, SPOTIFY_REDIRECT_URI

auth_bp = Blueprint('auth', __name__)

spotify = oauth.create_client('spotify')

@auth_bp.route('/login')
def login():
    redirect_uri = SPOTIFY_REDIRECT_URI
    return spotify.authorize_redirect(redirect_uri)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/callback')
def callback():
    token = spotify.authorize_access_token()
    resp = spotify.get('me')
    user_info = resp.json()
    
    session['user'] = user_info

    return f"Olá, {user_info['display_name']}! Seu e-mail é: {user_info['email']}"
