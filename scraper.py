def get_recommendations(client, genres, artists, limit):
    songs = client.recommendations(seed_artists=artists, seed_genres=genres, limit=limit)
    return songs