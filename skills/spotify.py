"""Spotify music control skill for Wednesday."""

import os
import sys

if sys.platform == "win32":
    from skills import BaseSkill
else:
    from . import BaseSkill


class Skill(BaseSkill):
    """Control Spotify playback — play, pause, skip, volume, search."""

    name = "Spotify"
    description = "Control Spotify: play songs/artists/playlists, pause, skip, adjust volume"

    SCOPES = " ".join([
        "user-modify-playback-state",
        "user-read-playback-state",
        "user-read-currently-playing",
    ])

    def __init__(self):
        self._sp = None

    def _client(self):
        """Lazy-init Spotify client with OAuth."""
        if self._sp is not None:
            return self._sp

        try:
            import spotipy
            from spotipy.oauth2 import SpotifyOAuth
        except ImportError:
            raise RuntimeError("spotipy not installed — run: pip install spotipy")

        client_id = os.getenv("SPOTIFY_CLIENT_ID", "")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "")
        redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

        if not client_id or client_id == "your_spotify_client_id_here":
            raise RuntimeError(
                "Spotify not configured. Add SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET to .env. "
                "Create an app at https://developer.spotify.com/dashboard and set the redirect URI to "
                "http://127.0.0.1:8888/callback (Spotify no longer accepts localhost)"
            )

        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=self.SCOPES,
            cache_path=".spotify_token_cache",
            open_browser=True,
        )
        self._sp = spotipy.Spotify(auth_manager=auth_manager)
        return self._sp

    def execute(self, args):
        action = args.get("action", "current")

        try:
            sp = self._client()
        except RuntimeError as e:
            return str(e)

        if action == "play":
            return self._play(sp, args.get("query", ""))
        elif action == "pause":
            return self._pause(sp)
        elif action == "resume":
            return self._resume(sp)
        elif action == "next":
            return self._next(sp)
        elif action == "previous":
            return self._previous(sp)
        elif action == "current":
            return self._current(sp)
        elif action == "volume":
            return self._volume(sp, args.get("level", 50))
        elif action == "search":
            return self._search(sp, args.get("query", ""))
        else:
            return f"Unknown Spotify action: {action}"

    def _play(self, sp, query):
        if not query:
            return self._resume(sp)

        results = sp.search(q=query, limit=1, type="track")
        tracks = results.get("tracks", {}).get("items", [])
        if not tracks:
            return f"No tracks found for: {query}"

        track = tracks[0]
        sp.start_playback(uris=[track["uri"]])
        artist = track["artists"][0]["name"]
        return f"Playing \"{track['name']}\" by {artist}"

    def _pause(self, sp):
        sp.pause_playback()
        return "Paused"

    def _resume(self, sp):
        sp.start_playback()
        return "Resumed"

    def _next(self, sp):
        sp.next_track()
        return "Skipped to next track"

    def _previous(self, sp):
        sp.previous_track()
        return "Going to previous track"

    def _current(self, sp):
        playing = sp.current_playback()
        if not playing or not playing.get("item"):
            return "Nothing is currently playing"
        item = playing["item"]
        artist = item["artists"][0]["name"]
        status = "Playing" if playing["is_playing"] else "Paused"
        return f"{status}: \"{item['name']}\" by {artist}"

    def _volume(self, sp, level):
        level = max(0, min(100, int(level)))
        sp.volume(level)
        return f"Volume set to {level}%"

    def _search(self, sp, query):
        if not query:
            return "No search query provided"
        results = sp.search(q=query, limit=5, type="track")
        tracks = results.get("tracks", {}).get("items", [])
        if not tracks:
            return f"No results for: {query}"
        lines = [f"Search results for \"{query}\":"]
        for i, t in enumerate(tracks, 1):
            artist = t["artists"][0]["name"]
            lines.append(f"  {i}. {t['name']} — {artist}")
        return "\n".join(lines)
