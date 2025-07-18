import os
import time
import win32com.client
from osop.osplayer import OSPlayer
from osop.filehandler import FileHandler
from util.playlist import Playlist

class A:
    def __init__(self):
        self.time = 0

    def currentTime(self):
        return self.time

class WindowsPlayer(OSPlayer):
    def __init__(self):
        super().__init__()
        self.wmp = win32com.client.Dispatch("WMPlayer.OCX")
        self.controls = None
        self.media = None

    def play(self, song_or_playlist):
        if isinstance(song_or_playlist, Playlist):
            self.playing_song = False
            self.playlist = song_or_playlist
            return self.play_song(self.playlist.request_next_track())
        else:
            self.playing_song = True
            return self.play_song(song_or_playlist)

    def play_song(self, uid):
        self.player = A()
        self.uid = uid
        audio_path = os.path.join(FileHandler.AUDIOS, f"{uid}.mp3")

        if not os.path.exists(audio_path):
            print(f"Audio file not found: {audio_path}")
            return False

        # Load metadata
        try:
            with open(os.path.join(FileHandler.SONG_DATA, f"{uid}.txt")) as f:
                self.title = f.readline().strip()
                self.artist = f.readline().strip()
                self.album = f.readline().strip()
                self.duration = float(f.readline().strip())
        except Exception as e:
            print(f"Error reading metadata: {e}")
            return False

        self.artwork_path = os.path.join(FileHandler.SONG_DATA, f"{uid}.png")

        self.media = self.wmp.newMedia(audio_path)
        self.wmp.currentPlaylist.clear()
        self.wmp.currentPlaylist.appendItem(self.media)
        self.wmp.controls.play()
        self.controls = self.wmp.controls
        self.paused = False
        return True

    def toggle_play_pause(self):
        if not self.controls:
            return
        if self.paused:
            self.controls.play()
        else:
            self.controls.pause()
        self.paused = not self.paused

    def seek(self, time):
        if self.controls:
            self.controls.currentPosition = float(time)

    def skip_forward(self, time):
        if self.controls:
            self.controls.currentPosition += float(time)

    def skip_backward(self, time):
        if self.controls:
            self.controls.currentPosition -= float(time)
            if self.controls.currentPosition < 0:
                self.controls.currentPosition = 0

    def next_track(self):
        if not self.playing_song:
            self.play_song(self.playlist.request_next_track())

    def previous_track(self):
        if not self.playing_song:
            self.play_song(self.playlist.request_last_track(self.controls.currentPosition if self.controls else 0.0))

    def update(self):
        if self.media and self.controls:
            if not self.paused and self.controls.currentPosition >= self.media.duration:
                if not self.playing_song:
                    self.play_song(self.playlist.request_next_track())
                else:
                    self.paused = True
            self.player.time = self.controls.currentPosition

    def stop(self):
        if self.controls:
            self.controls.stop()
        self.paused = True
        self.controls = None
        self.media = None
        self.player = None