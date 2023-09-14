import argparse
import logging
import datetime as dt
import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials
from pathlib import Path
from dotenv import load_dotenv
from scraper import get_recommendations, save_track
from spotipy import SpotifyException
from utils import setup_session, format_retry_after

# Scraping Settings
MAX_FAILED_SCRAPES = 100

# Create logs directory if it doesn't exist
Path('logs').mkdir(parents=True, exist_ok=True)

# Define logging directory
LOGGING_DIR = f'logs/spotify_scrape-{dt.datetime.today().strftime("%Y%m%d")}.log'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(LOGGING_DIR), encoding='utf-8'),
    ]
)

def main():
    load_dotenv()
    session, retry, adapter = setup_session()

    # Define command-line arguments and help messages
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

    # Create a Spotify client
    client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(), requests_session=session)
    consecutive_failed_scrapes = 0

    # Loop will run until request limit is reached or if consecutive failed scrapes passes MAX_FAILED_SCRAPES
    while args.limit > 0 and consecutive_failed_scrapes < MAX_FAILED_SCRAPES:
        curr_limit = 100 if args.limit > 100 else args.limit
        curr_scraped = 0

        # Get recommended tracks
        recommended_tracks = get_recommendations(client=client, genres=args.genre, artists=args.artist, limit=curr_limit)
        for track in recommended_tracks["tracks"]:
            current_payload = {
                "spotify_song_id": track["id"],
                "spotify_artist_id": track["artists"][0]["id"],
                "title": track["name"],
                "artist": track["artists"][0]["name"],
                "release_date": track["album"]["release_date"],
                "release_date_precision": track["album"]["release_date_precision"],
                "track_popularity": track["popularity"]
            }
            try:
                # Save track and check for success
                scrape_success = save_track(client=client, genres=args.genre, track_payload=current_payload)
            except SpotifyException as e:
                if e.http_status == 429:
                    # Status 429 means rate limit. This logs the value of the retry-after header.
                    formatted_retry_after = format_retry_after(int(e.headers['retry-after']))
                    logging.error(f"Rate limited for {formatted_retry_after}. Exiting script...")
                elif e.http_status == 500:
                    # Retry the request after a delay
                    logging.error("Spotify API returned a 500 error. Exiting script...")
                else:
                    logging.error(f"Unknown Spotify API error occurred. Exiting script...")
                exit()
            except:
                logging.error(f"Script lost connection. Exiting script...")
                exit()
            if scrape_success:
                curr_scraped+=1
                consecutive_failed_scrapes = 0
            else:
                consecutive_failed_scrapes+=1
        args.limit-=curr_scraped
        logging.info("Sleeping for 30 seconds to avoid rate limits...")
        time.sleep(30)
    if args.limit == 0:
        logging.info(f"Successfully scraped desired limit. Exiting script...")
    else:
        logging.info(f"Max failed scrapes exceeded. {args.limit} tracks left unscraped. Exiting script...")

if __name__ == '__main__':
    main()  