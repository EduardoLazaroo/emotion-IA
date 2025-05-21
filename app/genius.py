import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")
GENIUS_BASE_URL = "https://api.genius.com"

headers = {
    "Authorization": f"Bearer {GENIUS_API_TOKEN}"
}

def search_song_on_genius(song_title, artist):
    query = f"{song_title} {artist}"
    search_url = f"{GENIUS_BASE_URL}/search?q={quote(query)}"
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        hits = data.get("response", {}).get("hits", [])
        
        for hit in hits:
            result = hit["result"]
            if artist.lower() in result["primary_artist"]["name"].lower():
                return result["url"]
    except Exception as e:
        print(f"Erro ao buscar música no Genius: {e}")
    
    return None

def extract_lyrics_from_url(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        lyrics_div = soup.find("div", class_="lyrics")
        if lyrics_div:
            return lyrics_div.get_text().strip()

        lyrics_containers = soup.select("div[data-lyrics-container='true']")
        if lyrics_containers:
            return "\n".join([c.get_text(separator="\n").strip() for c in lyrics_containers])
    except Exception as e:
        print(f"Erro ao extrair letra do Genius: {e}")
    
    return None
