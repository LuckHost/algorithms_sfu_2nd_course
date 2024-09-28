"""Playlist"""

import pygame
from linked_list import LinkedList
from music_track import MusicTrack

class Playlist(LinkedList):
    """Class representing a music playlist. Inherits from a doubly linked list, 
    allowing for navigation through the tracks."""

    def __init__(self, data=None):
        """Initializes the playlist with optional data.
        
        Args:
            data: Optional initial data for the playlist, 
            can be None or a MusicTrack.
        """
        super().__init__(data)
        self._current = None

    def play_all(self, track) -> MusicTrack:
        """Plays all tracks starting from the provided track.
        
        Args:
            track (MusicTrack): The track from which to start playing.
        
        Returns:
            MusicTrack: The track that is currently playing.
        """
        self._current = track
        pygame.mixer.music.load(self.current.path)
        pygame.mixer.music.play()

    def next_track(self) -> MusicTrack:
        """Plays the next track in the playlist.
        
        If there is a next track in the list, 
        it moves to that track and starts playing.
        
        Returns:
            MusicTrack: The next track that is being played.
        """
        if self._current:
            self.play_all(self._current.next)

    def previous_track(self) -> MusicTrack:
        """Plays the previous track in the playlist.
        
        If there is a previous track in the list, 
        it moves to that track and starts playing.
        
        Returns:
            MusicTrack: The previous track that is being played.
        """
        if self._current:
            self.play_all(self._current.prev)

    @property
    def current(self):
        """Returns the currently playing track.
        
        Returns:
            MusicTrack: The current track that is playing, or None if no track is selected.
        """
        if not self._current:
            return None
        return self._current.data

    @current.setter
    def current(self, current):
        """Sets the current track to the given track.
        
        Args:
            current (MusicTrack): The track to set as currently playing.
        """
        self._current = current
