# 1. Song ID checked on csv if it exists. 
#     1a. If it exists
#         1a1. Move to next song
#     1b. If it does not exist
#         1.2a Get track features
#         1.3a Dump to csv 
# 2. Move to next song.
import csv
from pathlib import Path

SPOTIFY_DATASET_FILEPATH = "spotify_dataset.csv"

def csv_file_exists():
    return Path(SPOTIFY_DATASET_FILEPATH).is_file()

def get_recommendations(client, genres, artists, limit):
    recommended_songs = client.recommendations(seed_artists=artists, seed_genres=genres, limit=limit)
    return recommended_songs

def save_track(client, track_payload):
    if check_if_track_exists(track_payload["spotify_song_id"]):
        return 
    current_track_features = get_track_features(client, track_payload["spotify_song_id"])[0]
    current_track_features.pop("id")
    track_payload.update(current_track_features)
    fieldnames = ['spotify_song_id', 'title', 'artist'] + list(current_track_features.keys())
    if not csv_file_exists():
        with open(SPOTIFY_DATASET_FILEPATH, 'w', newline='') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()
    with open(SPOTIFY_DATASET_FILEPATH, 'a', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writerow(track_payload)

def get_track_features(client, spotify_song_id):
    current_track_features = client.audio_features(tracks=[spotify_song_id])
    return current_track_features

def check_if_track_exists(spotify_song_id):
    if not csv_file_exists():
        return False

    with open(SPOTIFY_DATASET_FILEPATH, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row['spotify_song_id'] == spotify_song_id:
                return True

    return False