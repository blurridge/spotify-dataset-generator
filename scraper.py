import csv
import datetime as dt
import logging
from pathlib import Path

SPOTIFY_DATASET_FILEPATH = "spotify_dataset.csv"
Path('./logs').mkdir(parents=True, exist_ok=True)
LOGGING_DIR = f'logs/spotify_scrape-{dt.datetime.today().strftime("%Y%m%d")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(LOGGING_DIR)),
    ]
)

def csv_file_exists():
    """
    Checks if dataset file exists.
    """
    return Path(SPOTIFY_DATASET_FILEPATH).is_file()

def get_recommendations(client, genres, artists, limit):
    """
    Scrapes from Spotify API via Spotipy recommended songs based on seed artists, genres, and a set limit.
    """
    recommended_songs = client.recommendations(seed_artists=artists, seed_genres=genres, limit=limit)
    return recommended_songs

def save_track(client, track_payload):
    """
    Saves track to the dataset if it passes duplication checks.
    """
    if check_if_track_exists(track_payload["spotify_song_id"]):
        logging.error(f"{track_payload['artist']} - {track_payload['title']} already exists in the dataset. Skipping...")
        return 
    logging.info(f"Scraping features for {track_payload['artist']} - {track_payload['title']}...")
    current_track_features = get_track_features(client, track_payload["spotify_song_id"])[0]
    current_track_features.pop("id")
    track_payload.update(current_track_features)
    fieldnames = ['spotify_song_id', 'title', 'artist'] + list(current_track_features.keys())
    if not csv_file_exists():
        logging.info(f"Dataset file not found. Creating new .csv file...")
        with open(SPOTIFY_DATASET_FILEPATH, 'w', newline='') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()
    with open(SPOTIFY_DATASET_FILEPATH, 'a', newline='', encoding='utf-8') as csvfile:
        logging.info(f"Adding {track_payload['artist']} - {track_payload['title']} to the dataset...")
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writerow(track_payload)

def get_track_features(client, spotify_song_id):
    """
    Scrapes track features from Spotify API via Spotipy. It describes the characteristics of the tracks.
    """
    current_track_features = client.audio_features(tracks=[spotify_song_id])
    return current_track_features

def check_if_track_exists(spotify_song_id):
    """
    Returns a boolean about the existence of the track in the current dataset.
    """
    if not csv_file_exists():
        return False

    with open(SPOTIFY_DATASET_FILEPATH, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row['spotify_song_id'] == spotify_song_id:
                return True

    return False