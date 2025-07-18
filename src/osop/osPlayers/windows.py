import os
import time
import win32com.client

from osop.osplayer import OSPlayer
from osop.filehandler import FileHandler
from util.playlist import Playlist

# For media session
from winrt.windows.media import MediaPlaybackType
from winrt.windows.media.systemmediatransportcontrols import (
    SystemMediaTransportControls,
    SystemMediaTransportControlsButton,
    SystemMediaTransportControlsPlaybackStatus,
)

class MediaSessionController:
    def __init__(self, player):
        self.player = player
        self.controls = SystemMediaTransportControls.get_for_current_view()
        self.controls.is_enabled = True
        self.controls.is_play_enabled = True
        self.controls.is_pause_enabled = True
        self.controls.is_next_enabled = True
        self.controls.is_previous_enabled = True
        self.controls.button_pressed += self._on_button_pressed

    def _on_button_pressed(self, sender, args):
        button = args.button
        if button == SystemMediaTransportControlsButton.play:
            self.player.toggle_play_pause()
        elif button == SystemMediaTransportControlsButton.pause:
            self.player.toggle_play_pause()
        elif button == SystemMediaTransportControlsButton.next:
            self.player.next_track()
        elif button == SystemMediaTransportControlsButton.previous:
            self.player.previous_track()

    def update_metadata(self):
        updater = self.controls.display_updater
        updater.type = MediaPlaybackType.music
        updater.music_properties.title = self.player.title
        updater.music_properties.artist = self.player.artist
        updater.music_properties.album_title = self.player.album
        updater.update()

        self.controls.playback_status = (
            SystemMediaTransportControlsPlaybackStatus.playing
            if not self.player.paused else
            SystemMediaTransportControlsPlaybackStatus.paused
        )


class WindowsOSPlayer(OSPlayer):
    def __init__(self):
        super().__init__()
        self.wmp = win32com.client.Dispatch("WMPlayer.OCX")
        self.controls = None
        self.media = None
        self.media_session = MediaSessionController(self)

    def play(self, song_or_playlist):
        if isinstance(song_or_playlist, Playlist):
            self.playing_song = False
            self.playlist = song_or_playlist
            return self.play_song(self.playlist.request_next_track())
        else:
            self.playing_song = True
            return self.play_song(song_or_playlist)

    def play_song(self, uid):
        self.uid = uid
        audio_path = os.path.join(FileHandler.AUDIOS, f"{uid}.mp3")

        if not os.path.exists(audio_path):
            print(f"Audio file not found: {audio_path}")
            return False

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

        self.media_session.update_metadata()
        return True

    def toggle_play_pause(self):
        if not self.controls:
            return
        if self.paused:
            self.controls.play()
        else:
            self.controls.pause()
        self.paused = not self.paused
        self.media_session.update_metadata()

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

    def stop(self):
        if self.controls:
            self.controls.stop()
        self.paused = True
        self.controls = None
        self.media = None
