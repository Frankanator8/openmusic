from downloader import VideoDownload
from filehandler import FileHandler

FileHandler.check_folder()

a = VideoDownload("undertale ost 071", search=True)
a.download()
print(a.uid)