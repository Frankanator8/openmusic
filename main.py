from downloader import VideoDownload
from filehandler import FileHandler

FileHandler.check_folder()

a = VideoDownload("marry you", search=True)
a.download()