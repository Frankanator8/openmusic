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
import time

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
        self.uid = ""
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
        self.command_center.nextTrackCommand().setEnabled_(False)
        self.command_center.previousTrackCommand().setEnabled_(False)

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

    def play(self, uid):
        self.uid = uid
        file_url = NSURL.fileURLWithPath_(f"{FileHandler.AUDIOS}/{uid}.mp3")

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

        # Update Now Playing info
        self.update_now_playing()

        return True

    def update_now_playing(self):
        """Update the Now Playing info center with current metadata and playback state"""
        if self.info_center and self.player:
            info = self._generate_info()
            self.info_center.setNowPlayingInfo_(info)

    def _handle_play(self, event):
        if self.player and not self.player.isPlaying():
            self.player.play()
            self.update_now_playing()
        return 0  # Return 0 for success

    def _handle_pause(self, event):
        if self.player and self.player.isPlaying():
            self.player.pause()
            self.update_now_playing()
        return 0  # Return 0 for success

    def _handle_toggle_play_pause(self, event):
        if not self.player:
            return 1  # Return 1 for failure

        if self.player.isPlaying():
            self.player.pause()
        else:
            self.player.play()

        self.update_now_playing()
        return 0  # Return 0 for success

    def _handle_seek(self, event):
        """Handle scrubbing/seeking to a specific position"""
        if not self.player:
            return 1

        try:
            # Get the requested playback position from the event
            requested_time = event.positionTime()

            # Clamp the time to valid bounds
            max_time = self.duration
            seek_time = max(0.0, min(requested_time, max_time))

            # Set the player's current time
            self.player.setCurrentTime_(seek_time)

            # Update Now Playing info immediately
            self.update_now_playing()

            return 0
        except Exception as e:
            print(f"Error seeking: {e}")
            return 1

    def _handle_skip_forward(self, event):
        """Handle skip forward (fast forward) button"""
        if not self.player:
            return 1

        try:
            # Get skip interval from event, default to 15 seconds
            skip_interval = 15.0
            if hasattr(event, 'interval') and event.interval():
                skip_interval = event.interval()

            current_time = self.player.currentTime()
            new_time = min(current_time + skip_interval, self.duration)

            self.player.setCurrentTime_(new_time)
            self.update_now_playing()

            return 0
        except Exception as e:
            print(f"Error skipping forward: {e}")
            return 1

    def _handle_skip_backward(self, event):
        """Handle skip backward (rewind) button"""
        if not self.player:
            return 1

        try:
            # Get skip interval from event, default to 15 seconds
            skip_interval = 15.0
            if hasattr(event, 'interval') and event.interval():
                skip_interval = event.interval()

            current_time = self.player.currentTime()
            new_time = max(current_time - skip_interval, 0.0)

            self.player.setCurrentTime_(new_time)
            self.update_now_playing()

            return 0
        except Exception as e:
            print(f"Error skipping backward: {e}")
            return 1

# Usage
if __name__ == "__main__":
    player = OSPlayer()

    if player.play("7154757342874e538d44ee98c537a192"):
        print("Playback started successfully")
        print("Media controls now support:")
        print("- Play/Pause keys")
        print("- Time scrubbing/seeking")
        print("- Skip forward/backward (15 second intervals)")
        print("- Control Center integration")

        # Keep the app running and update Now Playing info periodically
        try:
            while True:
                player.update_now_playing()

                # Run the event loop for a short time to handle system events
                NSRunLoop.currentRunLoop().runUntilDate_(
                    NSDate.dateWithTimeIntervalSinceNow_(0.5)
                )

                # Optional: Check if playback has finished
                if player.player and not player.player.isPlaying() and player.player.currentTime() >= player.duration:
                    print("Playback finished")
                    break

        except KeyboardInterrupt:
            print("Stopping playback...")
            if player.player:
                player.player.stop()
    else:
        print("Failed to start playback")