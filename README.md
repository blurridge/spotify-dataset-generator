# Spotify Dataset Generator

## Context
The Spotify dataset generator is a software tool designed to extract and compile a comprehensive dataset of music tracks and their features from the Spotify platform. This tool leverages Spotify's extensive music database and recommendation system to scrape data based on user-defined seed genres and artists. The implementation typically involves using Spotify's Web API and Python programming language along with libraries like Spotipy to retrieve track information, including attributes such as tempo, danceability, energy, and more.

In today's music landscape, data-driven insights are crucial for artists, music industry professionals, and music enthusiasts alike. This dataset generator serves as a valuable resource for various purposes. Music researchers can use it to study genre evolution, track popularity trends, and the impact of artists on specific genres. Playlist curators can harness this tool to create tailored playlists that cater to the musical preferences of their audience, thereby enhancing user engagement and satisfaction. Furthermore, machine learning enthusiasts can utilize the generated dataset to train recommendation algorithms, contributing to the development of more accurate and effective music discovery systems. Overall, this Spotify dataset generator bridges the gap between music data and actionable insights, making it an essential tool for the music industry and data analytics applications.

## Run Locally 
Clone the project

```bash
  git clone https://github.com/blurridge/spotify-dataset-generator
```

Go to the project directory

```bash
  cd spotify-dataset-generator
```

Create a virtual environment

```bash
  pip install virtualenv
  python3 -m venv env
```

Activate virtual environment

```bash
  source env/bin/activate # Mac or Linux
  env/Scripts/activate # Windows
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Create a `.env` file containing your Spotify API credentials. Use `.env.example` as a template.
```
  SPOTIPY_CLIENT_ID           = <<your spotify client id here>>
  SPOTIPY_CLIENT_SECRET       = <<your spotify client secret here>>
  SPOTIPY_REDIRECT_URI        = <<your spotify redirect uri here>>
```

## Arguments
```bash
options:
  -h, --help            show this help message and exit
  -g GENRE, --genre GENRE
                        The genre the recommender will use to scrape tracks. Comma separate different genres.
  -a ARTIST, --artist ARTIST
                        The artist the recommender will use to scrape tracks. Comma separate different Spotify IDs.
                        Use Spotify IDs of artist. Example: 2KC9Qb60EaY0kW4eH68vr3
  -l LIMIT, --limit LIMIT
                        The number of tracks the recommender will scrape
```