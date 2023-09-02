import argparse
import logging
import datetime as dt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pathlib import Path
from dotenv import load_dotenv
from scraper import get_recommendations, save_track

Path('logs').mkdir(parents=True, exist_ok=True)
LOGGING_DIR = f'logs/spotify_scrape-{dt.datetime.today().strftime("%Y%m%d")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(LOGGING_DIR)),
    ]
)

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(prog="Spotify Genre Track Scraper", 
                                     description="Gathers Spotify tracks' features from Spotify API using seeds",
                                     epilog="Script made by @blurridge || Zach Riane I. Machacon"
                                     )
    parser.add_argument("-g", "--genre", required=True, type=lambda s: s.split(","),
                        help="The genre the recommender will use to scrape tracks. Comma separate different genres.")
    parser.add_argument("-a", "--artist", required=True, type=lambda s: s.split(","),
                        help="""The artist the recommender will use to scrape tracks. Comma separate different Spotify IDs. 
                        Use Spotify IDs of artist. Example: 2KC9Qb60EaY0kW4eH68vr3""")
    parser.add_argument("-l", "--limit", type=int, required=True, 
                        help="The number of tracks the recommender will scrape")
    args = parser.parse_args()
    client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    while args.limit > 0:
        curr_limit = 100 if args.limit > 100 else args.limit
        recommended_tracks = get_recommendations(client=client, genres=args.genre, artists=args.artist, limit=curr_limit)
        for track in recommended_tracks["tracks"]:
            current_payload = {
                "spotify_song_id": track["id"],
                "title": track["name"],
                "artist": track["artists"][0]["name"],
            }
            save_track(client, current_payload)
        args.limit-=100

if __name__ == '__main__':
    main()  