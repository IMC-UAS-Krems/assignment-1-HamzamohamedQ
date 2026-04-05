# This module defines the Playlist and CollaborativePlaylist classes, which represent user-created playlists in the music streaming service.
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .tracks import Track
    from .users import User


class Playlist:
   

    def __init__(self, playlist_id: str, name: str, owner: "User"):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks: List["Track"] = []

    def add_track(self, track: "Track") -> None:
        
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_id: str) -> None:
        
        for i, t in enumerate(self.tracks):
            if t.track_id == track_id:
                del self.tracks[i]
                return

    def total_duration_seconds(self) -> int:
        """Total duration of all tracks in seconds."""
        return sum(t.duration_seconds for t in self.tracks)


class CollaborativePlaylist(Playlist):
    

    def __init__(self, playlist_id: str, name: str, owner: "User"):
        super().__init__(playlist_id, name, owner)
        self.contributors: List["User"] = [owner]

    def add_contributor(self, user: "User") -> None:
       
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user: "User") -> None:
        """Remove a contributor (cannot remove owner)."""
        if user != self.owner and user in self.contributors:
            self.contributors.remove(user)