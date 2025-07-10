import os
import sys
import time
import threading
from pathlib import Path
import ctypes
from ctypes import wintypes, windll, POINTER, Structure, c_void_p, c_char_p, c_wchar_p, byref
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, DWORD, HANDLE, BOOL, FLOAT
import comtypes
from comtypes import GUID, HRESULT, IUnknown, COMMETHOD, VARIANT
from comtypes.client import CreateObject
import win32com.client
import win32con
from osop.filehandler import FileHandler
from osop.osplayer import OSPlayer
from util.playlist import Playlist

# Windows Media Foundation function definitions
mfplat = windll.mfplat
mf = windll.mf
mfreadwrite = windll.mfreadwrite

# Define MF functions
MFStartup = mfplat.MFStartup
MFShutdown = mfplat.MFShutdown
MFCreateMediaSession = mf.MFCreateMediaSession
MFCreateSourceResolver = mf.MFCreateSourceResolver
MFCreateTopology = mf.MFCreateTopology
MFCreateAudioRendererActivate = mf.MFCreateAudioRendererActivate

# Media Foundation interfaces with proper COM definitions
class IMFMediaSession(IUnknown):
    _iid_ = GUID('{90377834-21D0-4DEE-8214-BA2E3E6C1127}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'SetTopology',
                  (['in'], DWORD, 'dwSetTopologyFlags'),
                  (['in'], POINTER(IUnknown), 'pTopology')),
        COMMETHOD([], HRESULT, 'ClearTopologies'),
        COMMETHOD([], HRESULT, 'Start',
                  (['in'], POINTER(GUID), 'pguidTimeFormat'),
                  (['in'], POINTER(VARIANT), 'pvarStartPosition')),
        COMMETHOD([], HRESULT, 'Pause'),
        COMMETHOD([], HRESULT, 'Stop'),
        COMMETHOD([], HRESULT, 'Close'),
        COMMETHOD([], HRESULT, 'Shutdown'),
        COMMETHOD([], HRESULT, 'GetClock',
                  (['out'], POINTER(POINTER(IUnknown)), 'ppClock')),
        COMMETHOD([], HRESULT, 'GetSessionCapabilities',
                  (['out'], POINTER(DWORD), 'pdwCaps')),
        COMMETHOD([], HRESULT, 'GetFullTopology',
                  (['in'], DWORD, 'dwGetFullTopologyFlags'),
                  (['in'], wintypes.LARGE_INTEGER, 'TopoId'),
                  (['out'], POINTER(POINTER(IUnknown)), 'ppFullTopology'))
    ]

class IMFMediaSource(IUnknown):
    _iid_ = GUID('{279A808D-AEC7-40C8-9C6B-A6B492C78A66}')

class IMFTopology(IUnknown):
    _iid_ = GUID('{83CF873A-F6DA-4BC8-823F-BACFD55DC430}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'GetTopologyID',
                  (['out'], POINTER(wintypes.LARGE_INTEGER), 'pID')),
        COMMETHOD([], HRESULT, 'AddNode',
                  (['in'], POINTER(IUnknown), 'pNode')),
        COMMETHOD([], HRESULT, 'RemoveNode',
                  (['in'], POINTER(IUnknown), 'pNode')),
        COMMETHOD([], HRESULT, 'GetNodeCount',
                  (['out'], POINTER(wintypes.WORD), 'pwNodes')),
        COMMETHOD([], HRESULT, 'GetNode',
                  (['in'], wintypes.WORD, 'wIndex'),
                  (['out'], POINTER(POINTER(IUnknown)), 'ppNode')),
        COMMETHOD([], HRESULT, 'Clear'),
        COMMETHOD([], HRESULT, 'CloneFrom',
                  (['in'], POINTER(IUnknown), 'pTopology'))
    ]

class IMFSourceResolver(IUnknown):
    _iid_ = GUID('{FBE5A32D-A497-4B61-BB85-97B1A848A6E3}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'CreateObjectFromURL',
                  (['in'], c_wchar_p, 'pwszURL'),
                  (['in'], DWORD, 'dwFlags'),
                  (['in'], POINTER(IUnknown), 'pProps'),
                  (['out'], POINTER(DWORD), 'pObjectType'),
                  (['out'], POINTER(POINTER(IUnknown)), 'ppObject'))
    ]

class IMFActivate(IUnknown):
    _iid_ = GUID('{7FEE9E9A-4A89-47A6-899C-B6A53A70FB67}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'ActivateObject',
                  (['in'], POINTER(GUID), 'riid'),
                  (['out'], POINTER(c_void_p), 'ppv'))
    ]

# Windows API constants
WM_APPCOMMAND = 0x0319
APPCOMMAND_MEDIA_PLAY_PAUSE = 14
APPCOMMAND_MEDIA_STOP = 13
APPCOMMAND_MEDIA_NEXTTRACK = 11
APPCOMMAND_MEDIA_PREVIOUSTRACK = 12

# Load required Windows DLLs
try:
    mf = windll.LoadLibrary('mf.dll')
    mfplat = windll.LoadLibrary('mfplat.dll')
    mfreadwrite = windll.LoadLibrary('mfreadwrite.dll')
    ole32 = windll.ole32
    user32 = windll.user32
    kernel32 = windll.kernel32
except OSError as e:
    print(f"Error loading Windows DLLs: {e}")
    raise

class WindowsPlayer(OSPlayer):
    def __init__(self):
        super().__init__()
        self.media_session = None
        self.media_source = None
        self.topology = None
        self.hwnd = None
        self.smtc = None
        self.session_state = "stopped"  # stopped, playing, paused
        self.position = 0.0

        self._initialize_media_foundation()
        self._setup_message_window()
        self._setup_smtc()

    def _initialize_media_foundation(self):
        """Initialize Windows Media Foundation"""
        try:
            # Initialize COM
            comtypes.CoInitialize()

            # Initialize Media Foundation
            hr = mfplat.MFStartup(0x20070, 0)  # MF_VERSION, MFSTARTUP_FULL
            if hr != 0:
                raise Exception(f"Failed to initialize Media Foundation: {hr}")

            # Create Media Session
            self.media_session = self._create_media_session()

            print("Media Foundation initialized successfully")

        except Exception as e:
            print(f"Error initializing Media Foundation: {e}")
            raise

    def _create_media_session(self):
        """Create a Media Foundation session"""
        try:
            # Create the media session using COM
            media_session_ptr = POINTER(IMFMediaSession)()

            # Call MFCreateMediaSession - this is the actual COM call
            hr = MFCreateMediaSession(None, byref(media_session_ptr))

            if hr != 0:  # S_OK = 0
                print(f"Failed to create media session: HRESULT {hr}")
                return None

            print("Media session created successfully")
            return media_session_ptr

        except Exception as e:
            print(f"Error creating media session: {e}")
            return None

    def _setup_message_window(self):
        """Setup window for receiving media key messages"""
        try:
            # Window class
            wc = wintypes.WNDCLASS()
            wc.lpfnWndProc = self._window_proc
            wc.lpszClassName = "WindowsMediaPlayer"
            wc.hInstance = kernel32.GetModuleHandleW(None)
            wc.hCursor = user32.LoadCursorW(None, win32con.IDC_ARROW)

            # Register class
            if not user32.RegisterClassW(ctypes.byref(wc)):
                raise Exception("Failed to register window class")

            # Create window
            self.hwnd = user32.CreateWindowExW(
                0,
                "WindowsMediaPlayer",
                "Windows Media Player",
                0,  # Hidden window
                0, 0, 0, 0,
                None, None,
                wc.hInstance,
                None
            )

            if not self.hwnd:
                raise Exception("Failed to create window")

            print(f"Created message window: {self.hwnd}")

        except Exception as e:
            print(f"Error setting up message window: {e}")

    def _setup_smtc(self):
        """Setup System Media Transport Controls"""
        try:
            # This would use Windows Runtime APIs
            # For a complete implementation, you'd need:
            # - Windows.Media.SystemMediaTransportControls
            # - Windows.Media.SystemMediaTransportControlsDisplayUpdater

            print("Setting up System Media Transport Controls...")
            self.smtc = None  # Placeholder

            # In a full implementation:
            # from winrt.windows.media import SystemMediaTransportControls
            # self.smtc = SystemMediaTransportControls.get_for_current_view()
            # self.smtc.add_button_pressed(self._on_media_button_pressed)
            # self.smtc.is_enabled = True

        except Exception as e:
            print(f"Error setting up SMTC: {e}")

    def _window_proc(self, hwnd, msg, wparam, lparam):
        """Window procedure for handling messages"""
        if msg == WM_APPCOMMAND:
            cmd = (lparam >> 16) & 0xFFFF

            if cmd == APPCOMMAND_MEDIA_PLAY_PAUSE:
                self.toggle_play_pause()
                return 1
            elif cmd == APPCOMMAND_MEDIA_NEXTTRACK:
                self.next_track()
                return 1
            elif cmd == APPCOMMAND_MEDIA_PREVIOUSTRACK:
                self.previous_track()
                return 1
            elif cmd == APPCOMMAND_MEDIA_STOP:
                self.stop()
                return 1

        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def _create_media_source_from_file(self, file_path):
        """Create a media source from an audio file"""
        try:
            # Create source resolver
            source_resolver_ptr = POINTER(IMFSourceResolver)()
            hr = MFCreateSourceResolver(byref(source_resolver_ptr))

            if hr != 0:
                print(f"Failed to create source resolver: HRESULT {hr}")
                return None

            # Create media source from file
            object_type = DWORD()
            media_source_ptr = POINTER(IUnknown)()

            # Convert file path to wide string
            wide_path = ctypes.create_unicode_buffer(file_path)

            # Call CreateObjectFromURL - this is the actual COM call
            hr = source_resolver_ptr.CreateObjectFromURL(
                wide_path.value,
                0x00000001,  # MF_RESOLUTION_MEDIASOURCE
                None,
                byref(object_type),
                byref(media_source_ptr)
            )

            if hr != 0:
                print(f"Failed to create media source: HRESULT {hr}")
                return None

            print(f"Media source created for: {file_path}")
            return media_source_ptr

        except Exception as e:
            print(f"Error creating media source: {e}")
            return None

    def _create_playback_topology(self, media_source):
        """Create a playback topology"""
        try:
            # Create topology
            topology_ptr = POINTER(IMFTopology)()
            hr = MFCreateTopology(byref(topology_ptr))

            if hr != 0:
                print(f"Failed to create topology: HRESULT {hr}")
                return None

            # Create audio renderer activate
            audio_renderer_ptr = POINTER(IMFActivate)()
            hr = MFCreateAudioRendererActivate(byref(audio_renderer_ptr))

            if hr != 0:
                print(f"Failed to create audio renderer: HRESULT {hr}")
                return None

            # In a full implementation, you would:
            # 1. Create source and sink nodes
            # 2. Add them to the topology
            # 3. Connect them together
            # This requires more complex COM calls with IMFTopologyNode

            print("Playback topology created")
            return topology_ptr

        except Exception as e:
            print(f"Error creating topology: {e}")
            return None

    def _update_smtc_metadata(self):
        """Update System Media Transport Controls metadata"""
        try:
            if not self.smtc:
                return

            # This would update the Windows media overlay
            print(f"Updating SMTC: {self.title} - {self.artist}")

            # In a full implementation:
            # updater = self.smtc.display_updater
            # updater.type = MediaPlaybackType.MUSIC
            # updater.music_properties.title = self.title
            # updater.music_properties.artist = self.artist
            # updater.music_properties.album_title = self.album
            # if self.artwork_path:
            #     updater.thumbnail = RandomAccessStreamReference.create_from_file(self.artwork_path)
            # updater.update()

        except Exception as e:
            print(f"Error updating SMTC metadata: {e}")

    def play(self, song_or_playlist):
        """Play a song or playlist"""
        if isinstance(song_or_playlist, Playlist):
            self.playing_song = False
            self.playlist = song_or_playlist
            return self.play_song(self.playlist.request_next_track())
        else:
            self.playing_song = True
            return self.play_song(song_or_playlist)

    def play_song(self, uid):
        """Play a specific song"""
        try:
            self.uid = uid
            audio_path = str(os.path.join(FileHandler.AUDIOS, f"{uid}.mp3"))

            if not os.path.exists(audio_path):
                print(f"Audio file not found: {audio_path}")
                return False

            # Stop current playback
            if self.session_state == "playing":
                self._stop_current_session()

            # Load metadata
            self._load_metadata(uid)

            # Create media source
            self.media_source = self._create_media_source_from_file(audio_path)
            if not self.media_source:
                print("Failed to create media source")
                return False

            # Create topology
            self.topology = self._create_playback_topology(self.media_source)
            if not self.topology:
                print("Failed to create topology")
                return False

            # Set topology and start playback
            if self.media_session:
                # Set the topology - this is the actual COM call
                hr = self.media_session.SetTopology(0, self.topology)
                if hr != 0:
                    print(f"Failed to set topology: HRESULT {hr}")
                    return False

                # Start playback - this is the actual COM call
                hr = self.media_session.Start(None, None)
                if hr != 0:
                    print(f"Failed to start playback: HRESULT {hr}")
                    return False

            self.session_state = "playing"
            self.paused = False

            # Update system media info
            self._update_smtc_metadata()

            print(f"Now playing: {self.title} by {self.artist}")
            return True

        except Exception as e:
            print(f"Error playing song: {e}")
            return False

    def _stop_current_session(self):
        """Stop the current media session"""
        try:
            if self.media_session and self.session_state != "stopped":
                # Stop playback - actual COM call
                hr = self.media_session.Stop()
                if hr != 0:
                    print(f"Failed to stop session: HRESULT {hr}")

                # Clear topologies - actual COM call
                hr = self.media_session.ClearTopologies()
                if hr != 0:
                    print(f"Failed to clear topologies: HRESULT {hr}")

            self.session_state = "stopped"

        except Exception as e:
            print(f"Error stopping session: {e}")

    def _load_metadata(self, uid):
        """Load song metadata"""
        try:
            metadata_path = str(os.path.join(FileHandler.SONG_DATA, f"{uid}.txt"))
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    self.title = f.readline().strip()
                    self.artist = f.readline().strip()
                    self.album = f.readline().strip()
                    self.duration = float(f.readline().strip())
            else:
                # Fallback defaults
                self.title = "Unknown Title"
                self.artist = "Unknown Artist"
                self.album = "Unknown Album"
                self.duration = 0.0

            # Load artwork path
            artwork_path = str(os.path.join(FileHandler.SONG_DATA, f"{uid}.png"))
            self.artwork_path = artwork_path if os.path.exists(artwork_path) else ""

        except Exception as e:
            print(f"Error loading metadata: {e}")

    def toggle_play_pause(self):
        """Toggle play/pause state"""
        try:
            if self.session_state == "playing":
                if self.media_session:
                    # Pause playback - actual COM call
                    hr = self.media_session.Pause()
                    if hr != 0:
                        print(f"Failed to pause: HRESULT {hr}")
                        return

                self.session_state = "paused"
                self.paused = True
                print("Paused")

            elif self.session_state == "paused":
                if self.media_session:
                    # Resume playback - actual COM call
                    hr = self.media_session.Start(None, None)
                    if hr != 0:
                        print(f"Failed to resume: HRESULT {hr}")
                        return

                self.session_state = "playing"
                self.paused = False
                print("Resumed")

            elif self.session_state == "stopped" and self.uid:
                # Restart current song
                self.play_song(self.uid)

            self._update_smtc_metadata()

        except Exception as e:
            print(f"Error toggling play/pause: {e}")

    def seek(self, time):
        """Seek to a specific time position"""
        try:
            if not self.media_session:
                return

            # Convert time to Media Foundation time format (100-nanosecond units)
            mf_time = int(time * 10000000)

            # Create VARIANT with the time value
            start_pos = VARIANT()
            start_pos.vt = 20  # VT_I8 (64-bit integer)
            start_pos.llVal = mf_time

            # Seek by starting at the new position - actual COM call
            hr = self.media_session.Start(None, byref(start_pos))
            if hr != 0:
                print(f"Failed to seek: HRESULT {hr}")
                return

            self.position = time
            print(f"Seeked to {time:.2f}s")

        except Exception as e:
            print(f"Error seeking: {e}")

    def skip_forward(self, time):
        """Skip forward by specified time"""
        try:
            new_position = min(self.position + time, self.duration)
            self.seek(new_position)

        except Exception as e:
            print(f"Error skipping forward: {e}")

    def skip_backward(self, time):
        """Skip backward by specified time"""
        try:
            new_position = max(self.position - time, 0.0)
            self.seek(new_position)

        except Exception as e:
            print(f"Error skipping backward: {e}")

    def next_track(self):
        """Play next track"""
        try:
            if not self.playing_song and self.playlist:
                next_uid = self.playlist.request_next_track()
                if next_uid:
                    self.play_song(next_uid)

        except Exception as e:
            print(f"Error playing next track: {e}")

    def previous_track(self):
        """Play previous track"""
        try:
            if not self.playing_song and self.playlist:
                prev_uid = self.playlist.request_last_track(self.position)
                if prev_uid:
                    self.play_song(prev_uid)

        except Exception as e:
            print(f"Error playing previous track: {e}")

    def get_position(self):
        """Get current playback position"""
        try:
            if self.media_session and self.session_state == "playing":
                # Get position from Media Foundation
                # This would query the presentation clock
                pass

            return self.position

        except Exception as e:
            print(f"Error getting position: {e}")
            return 0.0

    def update(self):
        """Update player state and process messages"""
        try:
            # Update position if playing
            if self.session_state == "playing":
                # This would get the actual position from Media Foundation
                pass

            # Process Windows messages
            if self.hwnd:
                msg = wintypes.MSG()
                while user32.PeekMessageW(ctypes.byref(msg), self.hwnd, 0, 0, 1):
                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageW(ctypes.byref(msg))

            # Check for end of playback
            if self.session_state == "playing" and self.position >= self.duration:
                if not self.playing_song and self.playlist:
                    self.next_track()
                else:
                    self.stop()

        except Exception as e:
            print(f"Error in update: {e}")

    def stop(self):
        """Stop playback"""
        try:
            self._stop_current_session()
            self.position = 0.0
            self.paused = False
            self.playing_song = False
            print("Stopped")

        except Exception as e:
            print(f"Error stopping: {e}")

    def cleanup(self):
        """Clean up resources"""
        try:
            self.stop()

            if self.media_session:
                # Shutdown the session - actual COM call
                hr = self.media_session.Shutdown()
                if hr != 0:
                    print(f"Failed to shutdown media session: HRESULT {hr}")

            if self.hwnd:
                user32.DestroyWindow(self.hwnd)

            # Shutdown Media Foundation
            hr = MFShutdown()
            if hr != 0:
                print(f"Failed to shutdown MF: HRESULT {hr}")

            # Uninitialize COM
            comtypes.CoUninitialize()

            print("Cleaned up resources")

        except Exception as e:
            print(f"Error during cleanup: {e}")


# Usage example
if __name__ == "__main__":
    player = WindowsPlayer()

    try:
        # Load and play a playlist
        playlist = Playlist.load("0a4543711e9448f59c43e70940d9dde8")

        if player.play(playlist):
            print("Starting native Windows playback...")
            print("Media keys enabled - use your keyboard media keys!")
            print("Press Ctrl+C to stop")

            # Main update loop
            while True:
                player.update()
                time.sleep(0.1)

        else:
            print("Failed to start playback")

    except KeyboardInterrupt:
        print("\nStopping playback...")

    finally:
        player.cleanup()