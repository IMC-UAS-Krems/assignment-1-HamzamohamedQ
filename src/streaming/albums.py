#album class 
from typing import List, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from .tracks import AlbumTrack
    from .artists import Artist


class Album:
    

    def __init__(self, album_id: str, title: str, artist: "Artist", release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks: List["AlbumTrack"] = []
        self._track_ids: Set[str] = set()
        self._duration_seconds = 0

    def add_track(self, track: "AlbumTrack") -> None:        
        # Set the track's album reference to this album
        track.album = self
        # Insert in correct position based on track_number
        inserted = False
        for i, t in enumerate(self.tracks):
            if track.track_number < t.track_number:
                self.tracks.insert(i, track)
                inserted = True
                break
        if not inserted:
            self.tracks.append(track)
        # Update track_ids set and duration
        self._track_ids.add(track.track_id)
        self._duration_seconds += track.duration_seconds

    def track_ids(self) -> Set[str]:
        
        return self._track_ids

    def duration_seconds(self) -> int:
        
        return self._duration_seconds