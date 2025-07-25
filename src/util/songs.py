import os
import shutil
import uuid

import moviepy

from osop.filehandler import FileHandler


class Songs:
    # Saves tuples of song data to prevent dupes
    cache = {}

    # Find all songs added. Alphabet returns the list in alphabetical order. Force no cache forces reload from disk.
    @classmethod
    def retrieve_songs(cls, alphabet=True, force_no_cache=False):
        songs = []
        if cls.cache == {} or force_no_cache:
            song_lib = {}
            song_name = {}
            for file in os.listdir(FileHandler.SONG_DATA):
                if file != ".DS_Store":
                    uid = file.split(".")[0]
                    if uid not in song_lib.keys():
                        song_lib[uid] = [False, False, False]

                    if file.endswith(".txt"):
                        song_lib[uid][0] = True
                        if alphabet:
                            _, _, name, _, _ = cls.load_song_data(uid)
                            song_name[uid] = name

                    if file.endswith(".png"):
                        song_lib[uid][1] = True

            for file in os.listdir(FileHandler.AUDIOS):
                if file != ".DS_Store":
                    uid = file.split(".")[0]
                    song_lib[uid][2] = True

            for key, value in song_lib.items():
                if all(value):
                    songs.append(key)
                    if key not in cls.cache.keys():
                        cls.load_song_data(key)

            if alphabet:
                songs.sort(key=lambda x: song_name[x])

        else:
            for key in cls.cache.keys():
                songs.append(key)

            if alphabet:
                songs.sort(key=lambda x: cls.cache[x][2])

        return songs

    # Creates song using the parameters
    @classmethod
    def make_song(cls, song_name, artist, album, image_url, audio_url):
        uid = cls.make_uid()
        cls.edit_song(uid, song_name, artist, album, image_url, audio_url)

    # Creates a unique id for songs/playlists/anything that needs it using uuid's
    @classmethod
    def make_uid(cls):
        return str(uuid.uuid4()).replace("-", "")

    # Edits a song. Different from make_song in that it requires a uid
    @classmethod
    def edit_song(cls, uid, song_name, artist, album, image_url, audio_url):
        clip = moviepy.AudioFileClip(audio_url)
        with open(os.path.join(FileHandler.SONG_DATA, f"{uid}.txt"), "w") as f:
            f.write(f"{song_name}\n{artist}\n{album}\n{clip.duration}")

        if audio_url != str(os.path.join(FileHandler.AUDIOS, f"{uid}.mp3")):
            clip.write_audiofile(str(os.path.join(FileHandler.AUDIOS, f"{uid}.mp3")))
        if image_url != str(os.path.join(FileHandler.SONG_DATA, f"{uid}.png")):
            shutil.copyfile(image_url, str(os.path.join(FileHandler.SONG_DATA, f"{uid}.png")))

        cls.cache[uid] = (image_url, audio_url, song_name, artist, album)

    # Loads the image, audio, title, artist, and album for a song
    @classmethod
    def load_song_data(cls, uid):
        if uid in cls.cache.keys():
            return cls.cache[uid]

        else:
            image_url = str(os.path.join(FileHandler.SONG_DATA, f"{uid}.png"))
            audio_url = str(os.path.join(FileHandler.AUDIOS, f"{uid}.mp3"))
            with open(os.path.join(FileHandler.SONG_DATA, f"{uid}.txt")) as f:
                title = f.readline().strip()
                artist = f.readline().strip()
                album = f.readline().strip()

            cls.cache[uid] = (image_url, audio_url, title, artist, album)

            return image_url, audio_url, title, artist, album

    # Deletes a song from storage
    @classmethod
    def delete_song(cls, uid):
        os.remove(os.path.join(FileHandler.SONG_DATA, f"{uid}.txt"))
        os.remove(os.path.join(FileHandler.AUDIOS, f"{uid}.mp3"))
        os.remove(os.path.join(FileHandler.SONG_DATA, f"{uid}.png"))
        if uid in cls.cache.keys():
            del cls.cache[uid]