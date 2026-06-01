# World Cupify

**Find out which of your Spotify favourites would win in a head-to-head tournament.**

World Cupify takes your most-listened artists or tracks from Spotify and puts them in a bracket-style elimination tournament. You pick the winner of each battle, round by round, until only one remains.
Playing it with friends sparks conversations and might turn apparently easy choices into long
debates.

---

## What it does

- Connects to your Spotify account via OAuth
- Pulls your top artists or tracks from the last month, 6 months, or year
- Sets up a tournament bracket (2 to 32 participants)
- Presents each matchup with photos and names for you to choose from
- Crowns a winner at the end

---

## Tech stack

- **Backend**: Python, FastAPI
- **Templating**: Jinja2
- **Auth**: Spotify OAuth 2.0 via Spotipy
- **Frontend**: HTML, CSS, vanilla JavaScript

---

## Running it locally

### 1. Clone the repo

```bash
git clone https://github.com/FranciscoNM-dev/spotify-worldCup
cd spotify-worldCup
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows (Git Bash)
source .venv/bin/activate       # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your Spotify app

Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and create an app. Set the redirect URI to:

```
http://localhost:8000/callback
```

### 5. Create a `.env` file

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8000/callback
```

### 6. Run the app

```bash
uvicorn src.api:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Project structure

```
spotify-worldCup/
├── src/
│   ├── api.py           # FastAPI endpoints
│   ├── auth.py          # Spotify OAuth logic
│   ├── spotifydata.py   # Data fetching and processing
│   └── tournament.py   # Implements the tournament logic
├── templates/           # Jinja2 HTML templates
├── static/              # CSS and JS files
├── requirements.txt
└── .env                 # Not included in the repo
```

---

## Notes

- Your Spotify data never leaves your session — nothing is stored on any server.
- The app requires the `user-top-read` scope to access your listening history.
- Token refresh is handled automatically, so you won't get logged out mid-tournament.

---

## Author

Made by [Francisco NM](https://github.com/FranciscoNM-dev)