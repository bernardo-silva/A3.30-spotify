""" Create a Spotify playlist with the tracks from A3.30"""
from dotenv import load_dotenv
import bs4
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_a3_30():
    """Get the tracks and artists from the Antena 3 website."""
    url = "https://media.rtp.pt/antena3/"
    result = requests.get(url, timeout=5)
    soup = bs4.BeautifulSoup(result.content, "html.parser")
    a330_url = soup.find("a", "results-right").get("href")

    result = requests.get(a330_url, timeout=5)
    soup = bs4.BeautifulSoup(result.content, "html.parser")

    tracks = [p.text for p in soup.find_all("p", "vote-track-name")]
    artists = [span.text for span in soup.find_all("span", "vote-band-title")]

    return tracks, artists


def create_playlist(tracks, artists):
    """Create a playlist on Spotify with the given tracks and artists."""
    scope = [
        "playlist-read-private",
        "playlist-modify-private",
        "playlist-read-collaborative",
        "playlist-modify-public",
    ]
    auth_manager = SpotifyOAuth(scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlists = sp.current_user_playlists()
    for playlist in playlists["items"]:
        if playlist["name"] == "A3.30":
            break

    track_ids = []
    for track, artist in zip(tracks, artists):
        print(f"Searching for {track} - {artist}")
        new_track = sp.search(q=f"{artist} {track}")["tracks"]["items"][0]
        track_ids.append(new_track["id"])

    sp.playlist_add_items(playlist["id"], items=track_ids)

def main():
    load_dotenv()
    tracks, artists = get_a3_30()
    create_playlist(tracks, artists)

if __name__ == "__main__":
    main()
