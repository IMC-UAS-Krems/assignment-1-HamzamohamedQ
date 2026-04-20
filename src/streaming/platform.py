# This module defines the StreamingPlatform class which manages the overall state of the music streaming service
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict

from .tracks import Track, Song
from .users import User, PremiumUser, FamilyAccountUser
from .artists import Artist
from .albums import Album
from .playlists import Playlist, CollaborativePlaylist
from .sessions import ListeningSession


class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self.catalogue_dict: Dict[str, Track] = {}
        self.user_dict: Dict[str, User] = {}
        self.artist_dict: Dict[str, Artist] = {}
        self.albums_dict: Dict[str, Album] = {}
        self.playlist_dict: Dict[str, Playlist] = {}
        self.sessions_dict: Dict[str, ListeningSession] = {}

    def add_track(self, track: Track) -> None:
        self.catalogue_dict[track.track_id] = track

    def add_user(self, user: User) -> None:
        self.user_dict[user.user_id] = user

    def add_artist(self, artist: Artist) -> None:
        self.artist_dict[artist.artist_id] = artist

    def add_album(self, album: Album) -> None:
        self.albums_dict[album.album_id] = album

    def add_playlist(self, playlist: Playlist) -> None:
        self.playlist_dict[playlist.playlist_id] = playlist

    def record_session(self, session: ListeningSession) -> None:
        self.sessions_dict[session.session_id] = session
        session.user.add_session(session)

    def get_track(self, track_id: str) -> Optional[Track]:
        return self.catalogue_dict.get(track_id)

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_dict.get(user_id)

    def get_artist(self, artist_id: str) -> Optional[Artist]:
        return self.artist_dict.get(artist_id)

    def get_album(self, album_id: str) -> Optional[Album]:
        return self.albums_dict.get(album_id)

    def all_users(self) -> List[User]:
        return list(self.user_dict.values())

    def all_tracks(self) -> List[Track]:
        return list(self.catalogue_dict.values())

    # Q1
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total_seconds = 0
        for session in self.sessions_dict.values():
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60.0

    # Q2
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        premium_users = [u for u in self.user_dict.values() if type(u).__name__ == "PremiumUser"]
        if not premium_users:
            return 0.0
        cutoff = datetime.now() - timedelta(days=days)
        total_unique = 0
        for user in premium_users:
            unique_tracks = set()
            for session in user.sessions:
                if session.timestamp >= cutoff:
                    unique_tracks.add(session.track.track_id)
            total_unique += len(unique_tracks)
        return total_unique / len(premium_users)

    # Q3
    def track_with_most_distinct_listeners(self) -> Optional[Track]:
        if not self.sessions_dict:
            return None
        listener_counts: Dict[str, Set[str]] = defaultdict(set)
        for session in self.sessions_dict.values():
            listener_counts[session.track.track_id].add(session.user.user_id)
        if not listener_counts:
            return None
        best_track_id = max(listener_counts.items(), key=lambda x: len(x[1]))[0]
        return self.get_track(best_track_id)

    # Q4
    def avg_session_duration_by_user_type(self) -> List[Tuple[str, float]]:
        type_sessions: Dict[str, List[int]] = defaultdict(list)
        for session in self.sessions_dict.values():
            user_type = type(session.user).__name__
            type_sessions[user_type].append(session.duration_listened_seconds)
        averages = [(t, sum(durs) / len(durs)) for t, durs in type_sessions.items()]
        averages.sort(key=lambda x: x[1], reverse=True)
        return averages

    # Q5
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        total_seconds = 0
        for user in self.user_dict.values():
            if isinstance(user, FamilyAccountUser):
                for sub in user.sub_users:
                    if sub.age < age_threshold:
                        total_seconds += sub.total_listening_seconds()
        return total_seconds / 60.0

    # Q6
    def top_artists_by_listening_time(self, n: int = 5) -> List[Tuple[Artist, float]]:
        artist_minutes: Dict[Artist, float] = defaultdict(float)
        for session in self.sessions_dict.values():
            track = session.track
            if isinstance(track, Song):
                artist = track.artist
                artist_minutes[artist] += session.duration_listened_minutes()  # method call
        sorted_artists = sorted(artist_minutes.items(), key=lambda x: x[1], reverse=True)
        return sorted_artists[:n]

    # Q7
    def user_top_genre(self, user_id: str) -> Optional[Tuple[str, float]]:
        user = self.get_user(user_id)
        if not user or not user.sessions:
            return None
        genre_minutes: Dict[str, float] = defaultdict(float)
        total = 0.0
        for session in user.sessions:
            genre = session.track.genre
            minutes = session.duration_listened_minutes()  # method call
            genre_minutes[genre] += minutes
            total += minutes
        if total == 0:
            return None
        top_genre, top_minutes = max(genre_minutes.items(), key=lambda x: x[1])
        percentage = (top_minutes / total) * 100.0
        return (top_genre, percentage)

    # Q8
    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> List[CollaborativePlaylist]:
        result = []
        for playlist in self.playlist_dict.values():
            if isinstance(playlist, CollaborativePlaylist):
                artists = set()
                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artists.add(track.artist)
                if len(artists) > threshold:
                    result.append(playlist)
        return result

    # Q9
    def avg_tracks_per_playlist_type(self) -> Dict[str, float]:
        counts = {"Playlist": 0, "CollaborativePlaylist": 0}
        totals = {"Playlist": 0, "CollaborativePlaylist": 0}
        for playlist in self.playlist_dict.values():
            type_name = type(playlist).__name__
            if type_name in counts:
                counts[type_name] += 1
                totals[type_name] += len(playlist.tracks)
        avg_playlist = totals["Playlist"] / counts["Playlist"] if counts["Playlist"] > 0 else 0.0
        avg_collab = totals["CollaborativePlaylist"] / counts["CollaborativePlaylist"] if counts["CollaborativePlaylist"] > 0 else 0.0
        return {"Playlist": avg_playlist, "CollaborativePlaylist": avg_collab}

    # Q10
    def users_who_completed_albums(self) -> List[Tuple[User, List[str]]]:
        result = []
        for user in self.all_users():
            user_track_ids = {s.track.track_id for s in user.sessions}
            completed_albums = []
            for album in self.albums_dict.values():
                if not album.tracks:
                    continue
                if album.track_ids().issubset(user_track_ids):  # method call
                    completed_albums.append(album.title)
            if completed_albums:
                result.append((user, completed_albums))
        return result