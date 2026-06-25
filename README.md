# SpotStats

A Python CLI tool that uses the Spotify API to display your top artists, tracks, and listening stats over an adjustable time period.

---

## Features

- View your top artists and tracks
- Adjustable time range (short, medium, or long term)

---

## Requirements

- Python 3.11+ (Recommended)
- A Spotify account
- A Spotify Developer app (for API credentials)

---

## Installation

**Option 1 — Clone the repository:**
```bash
git clone https://github.com/your-username/SpotStats.git
cd SpotStats
```

**Option 2 — Download the ZIP** from the repository page and extract it.

**Install dependencies:**
```bash
pip install spotipy
```

---

## Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and create an app to get your **Client ID** and **Client Secret**.
2. In the project directory, open the credentials file and enter your Client ID and Client Secret.

> **Never share your Client Secret publicly or commit it to GitHub.**

---

## How to Run

```bash
python main.py
```

Follow the on-screen prompts to select your desired time range and stat category.

---

## Tech Stack

- **Python**
- **[Spotipy](https://spotipy.readthedocs.io/)** — lightweight Spotify Web API wrapper

---

## License

This project is open source and available under the [MIT License](LICENSE).