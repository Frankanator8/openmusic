import os
import pathlib

from downloader import VideoDownload

# Path to the user's home directory
home = pathlib.Path.home()

# Construct the path to the Application Support folder
app_support_path = os.path.join(home, "Library", "Application Support")

# Print the path
print(f"The Application Support folder is located at: {app_support_path}")

a = VideoDownload("marry you bruno mars", search=True)
a.download()