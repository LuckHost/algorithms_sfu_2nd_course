from typing import Self

class MusicTrack:
    """Class representing a music track."""

    def __init__(self, path: str):
        """Initializes the music track 
        with a file path to the audio file.
        
        Args:
            path (str): The file path of the music track.
        """
        self.path = path

    def __eq__(self, other: Self) -> bool:
        """Checks if two music tracks are equal 
        based on their file path.
        
        Args:
            other (Self): Another instance of 
            `MusicTrack` to compare with.
        
        Returns:
            bool: True if the paths of the two 
            tracks are the same, False otherwise.
        """
        if other:
            return self.path == other.path
        return False
