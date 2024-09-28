"""Playlist module."""

import pygame
from linked_list import DoublyLinkedList
from music_track import MusicTrack


class Playlist(DoublyLinkedList):
    """Music playlist class."""

    def __init__(self, data=None):
        """Init method."""
        super().__init__(data)
        self._current = None

    def play_all(self, track) -> MusicTrack:
        """Play all tracks from the beginning of the playlist."""
        self._current = track
        pygame.mixer.music.load(self.current.path)
        pygame.mixer.music.play()

    def next_track(self) -> MusicTrack:
        """Play Previous track."""
        if self._current:
            self.play_all(self._current.next)

    def previous_track(self) -> MusicTrack:
        """Play Previous track."""
        if self._current:
            self.play_all(self._current.prev)

    @property
    def current(self):
        """Current track."""
        if not self._current:
            return None

        return self._current.data

    @current.setter
    def current(self, current):
        self._current = current
