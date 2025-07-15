from osop.filehandler import FileHandler
from util.playlist import Playlist

# Template of what an OSPlayer needs
class OSPlayer:
    def __init__(self):
        self.player = None
        self.title = ""
        self.artist = ""
        self.album = ""
        self.duration = 0.0
        self.artwork_path = ""
        self.uid = ""
        self.playing_song = False
        self.playlist = None
        self.paused = False

    def play(self, song_or_playlist):
        pass

    def play_song(self, uid):
        pass

    def toggle_play_pause(self):
        pass

    def seek(self, time):
        pass

    def skip_forward(self, time):
        pass

    def skip_backward(self, time):
        pass

    def next_track(self):
        pass

    def previous_track(self):
        pass

    def update(self):
        pass

    def stop(self):
        pass

    def cleanup(self):
        pass
