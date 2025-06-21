import os
import shutil
import uuid

import moviepy

from osop.filehandler import FileHandler


class SongLibrary:
    @classmethod
    def retrieve_songs(cls):
        song_lib = {}
        for file in os.listdir(FileHandler.SONG_DATA):
            if file != ".DS_Store":
                uid = file.split(".")[0]
                if uid not in song_lib.keys():
                    song_lib[uid] = [False, False, False]

                if file.endswith(".txt"):
                    song_lib[uid][0] = True

                if file.endswith(".png"):
                    song_lib[uid][1] = True

        for file in os.listdir(FileHandler.AUDIOS):
            if file != ".DS_Store":
                uid = file.split(".")[0]
                song_lib[uid][2] = True

        songs = []
        for key, value in song_lib.items():
            if all(value):
                songs.append(key)

        return songs

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