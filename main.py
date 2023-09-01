import argparse
import logging
import datetime as dt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pathlib import Path
from dotenv import load_dotenv
from scraper import get_recommendations

# Flow:
# 1. User enters args. 
# 2. Recommender will receive genre seed and artists. Will loop until limit
#     2a. If recommender returns tracks
#         2a1. Loop over each track
#         2a2. If track does not exist in csv, scrape and write to csv.
#         2a3. Else, skip.
#     2b. Return error 
# 3. END

# LOGGING_DIR = f'logs/spotify_scrape-{dt.datetime.today().strftime("%Y%m%d")}.log'

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)-8s %(message)s',
#     handlers=[
#         logging.StreamHandler(),
#         logging.FileHandler(Path(LOGGING_DIR)),
#     ]
# )

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(prog="Spotify Genre Track Scraper", 
                                     description="Gathers spotify tracks' features from Spotify API using seeds",
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
    recommended_songs = get_recommendations(client=client, genres=args.genre, artists=args.artist, limit=args.limit)

if __name__ == '__main__':
    main()  