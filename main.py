from downloader import VideoDownload
from filehandler import FileHandler

FileHandler.check_folder()

a = VideoDownload("idol yoasobi", search=True)
a.download()
print(a.uid)