from Foundation import NSURL, NSRunLoop, NSDate, NSNumber, NSString
from AVFoundation import AVAudioPlayer, AVAudioSession
from MediaPlayer import (
    MPNowPlayingInfoCenter,
    MPRemoteCommandCenter,
    MPMediaItemArtwork,
    MPNowPlayingInfoPropertyElapsedPlaybackTime,
    MPNowPlayingInfoPropertyPlaybackRate,
    MPMediaItemPropertyTitle,
    MPMediaItemPropertyArtist,
    MPMediaItemPropertyAlbumTitle,
    MPMediaItemPropertyPlaybackDuration,
    MPMediaItemPropertyArtwork
)
from AppKit import NSImage, NSApplication
from filehandler import FileHandler
from playlist import Playlist


class OSPlayer:
    def __init__(self):
        self.player = None
        self.info_center = MPNowPlayingInfoCenter.defaultCenter()
        self.command_center = MPRemoteCommandCenter.sharedCommandCenter()
        self.title = ""
        self.artist = ""
        self.album = ""
        self.duration = 0.0
        self.artwork = None
        self.artwork_path = ""
        self.uid = ""
        self.playing_song = False
        self.playlist = None
        self.paused = False
        self._setup_remote_commands()
        self._setup_audio_session()

    def _setup_audio_session(self):
        """Configure audio session for proper media key handling"""
        try:
            # Get the shared audio session
            session = AVAudioSession.sharedInstance()
            # Set category to playback to enable media controls
            session.setCategory_error_("AVAudioSessionCategoryPlayback", None)
            session.setActive_error_(True, None)
        except Exception as e:
            print(f"Warning: Could not set up audio session: {e}")

    def _setup_remote_commands(self):
        # Set up media key handlers
        self.command_center.playCommand().setEnabled_(True)
        self.command_center.pauseCommand().setEnabled_(True)
        self.command_center.togglePlayPauseCommand().setEnabled_(True)

        self.command_center.nextTrackCommand().setEnabled_(True)
        self.command_center.previousTrackCommand().setEnabled_(True)
        # Enable seeking and skip commands
        self.command_center.changePlaybackPositionCommand().setEnabled_(True)
        self.command_center.skipForwardCommand().setEnabled_(True)
        self.command_center.skipBackwardCommand().setEnabled_(True)

        # Set skip intervals (in seconds)
        self.command_center.skipForwardCommand().setPreferredIntervals_([NSNumber.numberWithFloat_(15.0)])
        self.command_center.skipBackwardCommand().setPreferredIntervals_([NSNumber.numberWithFloat_(15.0)])

        # Add handlers
        self.command_center.playCommand().addTargetWithHandler_(self._handle_play)
        self.command_center.pauseCommand().addTargetWithHandler_(self._handle_pause)
        self.command_center.togglePlayPauseCommand().addTargetWithHandler_(self._handle_toggle_play_pause)
        self.command_center.changePlaybackPositionCommand().addTargetWithHandler_(self._handle_seek)
        self.command_center.skipForwardCommand().addTargetWithHandler_(self._handle_skip_forward)
        self.command_center.skipBackwardCommand().addTargetWithHandler_(self._handle_skip_backward)
        self.command_center.nextTrackCommand().addTargetWithHandler_(self._handle_next_track)
        self.command_center.previousTrackCommand().addTargetWithHandler_(self._handle_previous_track)


    def _generate_info(self):
        if not self.player:
            return {}

        info = {
            MPMediaItemPropertyTitle: self.title,
            MPMediaItemPropertyArtist: self.artist,
            MPMediaItemPropertyAlbumTitle: self.album,
            MPNowPlayingInfoPropertyElapsedPlaybackTime: NSNumber.numberWithFloat_(self.player.currentTime()),
            MPNowPlayingInfoPropertyPlaybackRate: NSNumber.numberWithFloat_(1.0 if self.player.isPlaying() else 0.0),
            MPMediaItemPropertyPlaybackDuration: NSNumber.numberWithFloat_(self.duration)
        }

        if self.artwork:
            info[MPMediaItemPropertyArtwork] = self.artwork

        return info

    def play(self, song_or_playlist):
        if isinstance(song_or_playlist, Playlist):
            self.playing_song = False
            self.playlist = song_or_playlist
            self.command_center.skipForwardCommand().setEnabled_(False)
            self.command_center.skipBackwardCommand().setEnabled_(False)
            return self.play_song(self.playlist.request_next_track())

        else:
            self.playing_song = True
            self.command_center.skipForwardCommand().setEnabled_(True)
            self.command_center.skipBackwardCommand().setEnabled_(True)
            return self.play_song(song_or_playlist)

    def play_song(self, uid):
        self.uid = uid
        file_url = NSURL.fileURLWithPath_(f"{FileHandler.AUDIOS}/{uid}.mp3")

        if self.player and self.player.isPlaying():
            self.player.stop()

        # Create and play the audio player
        self.player = AVAudioPlayer.alloc().initWithContentsOfURL_error_(file_url, None)[0]

        if not self.player:
            print("Error loading audio file")
            return False

        self.player.prepareToPlay()

        # Load metadata
        try:
            with open(f"{FileHandler.SONG_DATA}/{uid}.txt") as f:
                self.title = f.readline().strip()
                self.artist = f.readline().strip()
                self.album = f.readline().strip()
                self.duration = float(f.readline().strip())
        except Exception as e:
            print(f"Error loading metadata: {e}")
            return False

        # Load artwork
        artwork_path = f"{FileHandler.SONG_DATA}/{uid}.png"
        self.artwork_path = artwork_path
        try:
            image = NSImage.alloc().initWithContentsOfFile_(artwork_path)
            if image:
                self.artwork = MPMediaItemArtwork.alloc().initWithBoundsSize_requestHandler_(
                    image.size(),
                    lambda size: image
                )
        except Exception as e:
            print(f"Error loading artwork: {e}")
            self.artwork = None

        # Start playback
        self.player.play()
        self.paused = False

        # Update Now Playing info
        self.update_now_playing()

        return True

    def update_now_playing(self):
        """Update the Now Playing info center with current metadata and playback state"""
        if self.info_center and self.player:
            info = self._generate_info()
            self.info_center.setNowPlayingInfo_(info)

        else:
            self.info_center.setNowPlayingInfo_({})

    def _handle_play(self, event):
        if self.player and not self.player.isPlaying():
            self.player.play()
            self.update_now_playing()
            self.paused = False
        return 0  # Return 0 for success

    def _handle_pause(self, event):
        if self.player and self.player.isPlaying():
            self.player.pause()
            self.update_now_playing()
            self.paused = True
        return 0  # Return 0 for success

    def _handle_toggle_play_pause(self, event):
        if not self.player:
            return 1  # Return 1 for failure

        self.toggle_play_pause()
        return 0  # Return 0 for success

    def toggle_play_pause(self):
        if self.player:
            if self.player.isPlaying():
                self.player.pause()
            else:
                self.player.play()
            self.paused = not self.paused
            self.update_now_playing()

    def _handle_seek(self, event):
        """Handle scrubbing/seeking to a specific position"""
        if not self.player:
            return 1

        try:
            # Get the requested playback position from the event
            requested_time = event.positionTime()

            self.seek(requested_time)

            return 0
        except Exception as e:
            print(f"Error seeking: {e}")
            return 1

    def seek(self, time):
        max_time = self.duration
        seek_time = max(0.0, min(time, max_time))

        # Set the player's current time
        self.player.setCurrentTime_(seek_time)

        # Update Now Playing info immediately
        self.update_now_playing()

    def _handle_skip_forward(self, event):
        """Handle skip forward (fast forward) button"""
        if not self.player:
            return 1

        try:
            # Get skip interval from event, default to 15 seconds
            skip_interval = 15.0
            if hasattr(event, 'interval') and event.interval():
                skip_interval = event.interval()

            self.skip_forward(skip_interval)

            return 0
        except Exception as e:
            print(f"Error skipping forward: {e}")
            return 1

    def skip_forward(self, time):
        current_time = self.player.currentTime()
        new_time = min(current_time + time, self.duration)

        self.player.setCurrentTime_(new_time)
        self.update_now_playing()

    def _handle_skip_backward(self, event):
        """Handle skip backward (rewind) button"""
        if not self.player:
            return 1

        try:
            # Get skip interval from event, default to 15 seconds
            skip_interval = 15.0
            if hasattr(event, 'interval') and event.interval():
                skip_interval = event.interval()

            self.skip_backward(skip_interval)

            return 0
        except Exception as e:
            print(f"Error skipping backward: {e}")
            return 1

    def skip_backward(self, time):
        current_time = self.player.currentTime()
        new_time = max(current_time - time, 0.0)

        self.player.setCurrentTime_(new_time)
        self.update_now_playing()

    def _handle_next_track(self, event):
        if not self.player:
            return 1

        try:
            self.next_track()
            return 0
        except Exception as e:
            print(f"Error skipping backward: {e}")
            return 1

    def next_track(self):
        if not self.playing_song:
            self.play_song(self.playlist.request_next_track())


    def _handle_previous_track(self, event):
        if not self.player:
            return 1

        try:
            self.previous_track()
            return 0
        except Exception as e:
            print(f"Error skipping forward: {e}")
            return 1

    def previous_track(self):
        if not self.playing_song:
            self.play_song(self.playlist.request_last_track(self.player.currentTime()))

    def update(self):
        self.update_now_playing()
        if self.player and not self.player.isPlaying() and not self.paused:
            if not self.playing_song:
                self.play_song(self.playlist.request_next_track())

            else:
                self.paused = True

# Usage
if __name__ == "__main__":
    playlist = Playlist.load("0a4543711e9448f59c43e70940d9dde8")
    player = OSPlayer()

    if player.play(playlist):
        # Keep the app running and update Now Playing info periodically
        try:
            while True:
                NSRunLoop.currentRunLoop().runUntilDate_(
                        NSDate.dateWithTimeIntervalSinceNow_(0.1)
                    )
                player.update()

        except KeyboardInterrupt:
            print("Stopping playback...")
            if player.player:
                player.player.stop()
    else:
        print("Failed to start playback")