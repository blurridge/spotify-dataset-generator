import csv
import datetime as dt
import logging
from pathlib import Path
from spotipy.client import Spotify

# Dataset Settings
SPOTIFY_DATASET_FILEPATH = "spotify_dataset.csv"

# Create logs directory if it doesn't exist
Path('./logs').mkdir(parents=True, exist_ok=True)
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

def csv_file_exists():
    """
    Checks if dataset file exists.
    """
    return Path(SPOTIFY_DATASET_FILEPATH).is_file()

def get_recommendations(client: Spotify, genres: list, artists: list, limit: int):
    """
    Scrapes from Spotify API via Spotipy recommended songs based on seed artists, genres, and a set limit.
    """
    recommended_songs = client.recommendations(seed_artists=artists, seed_genres=genres, limit=limit)
    return recommended_songs

def save_track(client: Spotify, genres: list, track_payload: dict):
    """
    Saves track to the dataset if it passes checks.
    """
    # Skips track if in dataset already
    if check_if_track_exists(track_payload["spotify_song_id"]): 
        logging.error(f"{track_payload['artist']} - {track_payload['title']} already exists in the dataset. Skipping...")
        return False
    
    # Skips track if doesn't match target genre
    logging.info(f"Checking if {track_payload['artist']} - {track_payload['title']} matches target genres...")
    if not check_if_artist_matches_genre(client=client, genres=genres, artist_id=track_payload['spotify_artist_id']): 
        logging.error(f"{track_payload['artist']} - {track_payload['title']} does not match genre. Skipping...")
        return False
    
    # Skips track if features are not scraped
    logging.info(f"Scraping features for {track_payload['artist']} - {track_payload['title']}...")
    current_track_features = get_track_features(client, track_payload["spotify_song_id"])[0]
    if current_track_features is None: 
        logging.error(f"{track_payload['artist']} - {track_payload['title']}'s features could not be scraped. Skipping...")
        return False
    
    current_track_features.pop("id")
    track_payload.update(current_track_features)
    fieldnames = list(track_payload.keys()) + list(current_track_features.keys())
    if not csv_file_exists():
        logging.info(f"Dataset file not found. Creating new .csv file...")
        with open(SPOTIFY_DATASET_FILEPATH, 'w', newline='') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()
    with open(SPOTIFY_DATASET_FILEPATH, 'a', newline='', encoding='utf-8') as csvfile:
        logging.info(f"Adding {track_payload['artist']} - {track_payload['title']} to the dataset...")
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writerow(track_payload)
    return True

def get_track_features(client:Spotify, spotify_song_id: str):
    """
    Scrapes track features from Spotify API via Spotipy. It describes the characteristics of the tracks.
    """
    current_track_features = client.audio_features(tracks=[spotify_song_id])
    return current_track_features

def check_if_track_exists(spotify_song_id: str):
    """
    Returns a boolean about the existence of the track in the current dataset.
    """
    if not csv_file_exists():
        return False
    with open(SPOTIFY_DATASET_FILEPATH, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row['spotify_song_id'] == spotify_song_id:
                return True
    return False

def check_if_artist_matches_genre(client:Spotify, genres: list, artist_id: str):
    """
    Checks if recommended song's artist matches one of the seed genres.
    """
    current_artists_genres = client.artist(artist_id)['genres']
    seed_genre_set = set(genres)

    # Uses nested loop since sometimes Spotify gives partial genres. This ensures matches with lists like [k-pop] and [k-pop girl group].
    for genre in seed_genre_set: 
        for artist_genre in current_artists_genres:
            if genre in artist_genre:
                return True
    return False