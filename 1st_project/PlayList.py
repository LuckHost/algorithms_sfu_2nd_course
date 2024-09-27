from LinkedList import LinkedList
from Composition import Composition
from pygame import mixer
import os

class PlayList(LinkedList):
    def __init__(self):
        super().__init__()
        self.playlists = {}

    def create_playlist(self, name: str):
        """Создать новый плейлист."""
        if name in self.playlists:
            print(f"Playlist {name} already exists.")
        else:
            self.playlists[name] = LinkedList()
            print(f"Playlist {name} created.")

    def delete_playlist(self, name: str):
        """Удалить плейлист."""
        if name in self.playlists:
            del self.playlists[name]
            print(f"Playlist {name} deleted.")
        else:
            print(f"Playlist {name} does not exist.")

    def add_track(self, playlist_name, track_path):
        """Добавить трек в плейлист."""
        if os.path.exists(track_path):
            self.playlists[playlist_name].append(track_path)
        else:
            print(f"Track {track_path} does not exist.")

    def remove_track(self, playlist_name, track_path):
        """Удалить трек из плейлиста."""
        try:
            self.playlists[playlist_name].remove(track_path)
        except ValueError:
            print(f"Track {track_path} not found in the playlist.")

    def move_track(self, playlist_name, track, new_position):
        """Переместить трек на новую позицию."""
        playlist = self.playlists.get(playlist_name, None)
        if playlist is None:
            print(f"Playlist {playlist_name} does not exist.")
            return

        if track not in playlist:
            print(f"Track {track} not found in the playlist.")
            return
        
        playlist.remove(track)
        playlist.insert(playlist[new_position], track)
        print(f"Moved track {track} to position {new_position} in playlist {playlist_name}.")

    def play_all(self, playlist_name):
        """Проигрывать плейлист циклически."""
        playlist = self.playlists.get(playlist_name, None)
        if playlist is None:
            print(f"Playlist {playlist_name} does not exist.")
            return

        current_track = playlist.first_item
        while True:
            self.play_track(current_track.data)
            current_track = current_track.next_item
            if current_track is None:
                current_track = playlist.first_item

    def play_track(self, track_path):
        """Проиграть один трек."""
        if os.path.exists(track_path):
            mixer.music.load(track_path)
            mixer.music.play()
        else:
            print(f"Track {track_path} does not exist.")
