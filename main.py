import argparse
import logging
import datetime as dt
from pathlib import Path

# Flow:
# 1. User enters args. 
# 2. Recommender will receive genre seed and artists. Will loop until limit
#     2a. If recommender returns tracks
#         2a1. Loop over each track
#         2a2. If track does not exist in csv, scrape and write to csv.
#         2a3. Else, skip.
#     2b. Return error 
# 3. END

# LOGGING_DIR = f'./logs/spotify_scrape-{dt.datetime.today().strftime("%Y%m%d")}.log'

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)-8s %(message)s',
#     handlers=[
#         logging.StreamHandler(),
#         logging.FileHandler(Path(LOGGING_DIR)),
#     ]
# )

def main():
    parser = argparse.ArgumentParser(prog="Spotify Genre Track Scraper", 
                                     description="Gathers spotify tracks' features from Spotify API using seeds",
                                     epilog="Script made by @blurridge || Zach Riane I. Machacon"
                                     )
    parser.add_argument("-g", "--genre", nargs='+', required=True, type=lambda s: [genre for genre in s.split(',')]
                        help="The genre the recommender will use to scrape tracks")
    parser.add_argument("-a", "--artist", nargs='+', required=True, type=lambda s: [artist for artist in s.split(',')]
                        help="The artist the recommender will use to scrape tracks")
    parser.add_argument("-l", "--limit", type=int, required=True, 
                        help="The number of tracks the recommender will scrape")
    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()