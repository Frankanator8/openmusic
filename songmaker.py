import shutil
import uuid

import moviepy

from filehandler import FileHandler


class SongMaker:
    @classmethod
    def make_song(cls, song_name, artist, album, image_url, audio_url):
        uid = cls.make_uid()
        cls.edit_song(uid, song_name, artist, album, image_url, audio_url)

    @classmethod
    def make_uid(cls):
        return str(uuid.uuid4()).replace("-", "")

    @classmethod
    def edit_song(cls, uid, song_name, artist, album, image_url, audio_url):
        clip = moviepy.AudioFileClip(audio_url)
        with open(f"{FileHandler.SONG_DATA}/{uid}.txt", "w") as f:
            f.write(f"{song_name}\n{artist}\n{album}\n{clip.duration}")

        if audio_url != f"{FileHandler.AUDIOS}/{uid}.mp3":
            clip.write_audiofile(f"{FileHandler.AUDIOS}/{uid}.mp3")
        if image_url != f"{FileHandler.SONG_DATA}/{uid}.png":
            shutil.copyfile(image_url, f"{FileHandler.SONG_DATA}/{uid}.png")