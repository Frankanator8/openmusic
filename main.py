from downloader import VideoDownload
from filehandler import FileHandler

FileHandler.check_folder()

a = VideoDownload("marry you bruno mars", search=True)
a.download()