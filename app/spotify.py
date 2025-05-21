import requests
from flask import current_app

def get_auth_url():
    client_id = current_app.config['CLIENT_ID']
    redirect_uri = current_app.config['REDIRECT_URI']
    scope = current_app.config['SCOPE'].replace(' ', '%20')

    return (
        'https://accounts.spotify.com/authorize'
        f'?client_id={client_id}'
        '&response_type=code'
        f'&redirect_uri={redirect_uri}'
        f'&scope={scope}'
    )

def get_token(code):
    token_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': current_app.config['REDIRECT_URI'],
        'client_id': current_app.config['CLIENT_ID'],
        'client_secret': current_app.config['CLIENT_SECRET']
    }
    token_response = requests.post(token_url, data=payload)
    return token_response.json()

def get_user_profile(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    user_response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    return user_response.json()

def get_current_track(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data and data.get('item'):
            track_name = data['item']['name']
            artists = ', '.join(artist['name'] for artist in data['item']['artists'])
            return f"{track_name} - {artists}"
    return "Nenhuma música tocando no momento."
