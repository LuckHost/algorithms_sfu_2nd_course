class Composition:
    def __init__(self, title: str, artist: str):
        self.title = title
        self.artist = artist

    def __str__(self):
        return f"{self.title} by {self.artist}"
