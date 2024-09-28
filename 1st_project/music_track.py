"""Music track module."""

from typing import Self


class MusicTrack():
    """Music track class"""
    def __init__(self, path: str):
        self.path = path

    def __eq__(self, other: Self) -> bool:
        if not other:
            return False

        return self.path == other.path
