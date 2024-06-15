import os
import platform
import subprocess
import sys
from io import StringIO
from formation import AppBuilder
import yt_dlp
import json
import ffmpeg
from tkinter import messagebox
import requests
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
ui_file = resource_path('UI.xml')
icon_file = resource_path('skibi.jpg')
app = AppBuilder(path=ui_file)
if not os.path.exists('downloaded_files'):
    os.makedirs('downloaded_files')
else:
    pass
def update_checker():
    requests.get()
def download_video(event=None):
    original_cwd = os.getcwd()
    os.chdir('downloaded_files')
    original_stderr = sys.stderr
    sys.stderr = StringIO()
    if app.audio.get():
        ydl_opts = {'extract_flat': 'discard_in_playlist',
 'final_ext': 'mp3',
 'format': 'bestaudio/best',
 'fragment_retries': 10,
 'ignoreerrors': 'only_download',
 'postprocessors': [{'key': 'FFmpegExtractAudio',
                     'nopostoverwrites': False,
                     'preferredcodec': 'mp3',
                     'preferredquality': '5'},
                    {'key': 'FFmpegConcat',
                     'only_multi_video': True,
                     'when': 'playlist'}],
 'retries': 10}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:   
            ydl.download(app.url.get())
    else:
        ydl_opts = {
            'extract_flat': 'discard_in_playlist',
            'format': 'mp4',
            'fragment_retries': 10,
            'ignoreerrors': 'only_download',
            'postprocessors': [{'key': 'FFmpegConcat',
                                'only_multi_video': True,
                                'when': 'playlist'}],
            'retries': 10
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(app.url.get())
    error_output = sys.stderr.getvalue()
    if error_output:
        sys.stderr = original_stderr
        messagebox.showerror("Error!", error_output)
    else:
        messagebox.showinfo("Done!", "Done downloading!")
    os.chdir(original_cwd)
def opendir(event=None):
    cwd = os.path.join(os.getcwd(), 'downloaded_files')
    system = platform.system()
    if system == 'Windows':
        subprocess.Popen(f'explorer "{cwd}"')
    elif system == 'Darwin':
        subprocess.Popen(['open', cwd])
    elif system == 'Linux':
        subprocess.Popen(['xdg-open', cwd])
    else:
        messagebox.showerror("Error", "Bruh what fucking system are you using lol")
    


        

app.connect_callbacks(globals())
app.mainloop()
