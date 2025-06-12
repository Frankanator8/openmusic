import shutil
import uuid

import moviepy

from filehandler import FileHandler


class SongMaker:
    @classmethod
    def make_song(cls, song_name, artist, album, image_url, audio_url):
        uid = cls.make_uid()
        clip = moviepy.AudioFileClip(audio_url)
        with open(f"{FileHandler.SONG_DATA}/{uid}.txt", "w") as f:
            f.write(f"{song_name}\n{artist}\n{album}\n{clip.duration}")

        clip.write_audiofile(f"{FileHandler.AUDIOS}/{uid}.mp3")
        shutil.copyfile(image_url, f"{FileHandler.SONG_DATA}/{uid}.png")

    @classmethod
    def make_uid(cls):
        return str(uuid.uuid4()).replace("-", "")