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
from packaging.version import Version

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

if os.path.exists('Skibidi Downloader Installer.exe'):
    os.remove('Skibidi Downloader Installer.exe')
else:
    pass

def update_checker():
    system = platform.system()
    if system == 'Windows':
        installed_ver = Version("1.0.3")
        response = requests.get("https://api.github.com/repos/1333481/SkibidiDownloader/releases/latest")
        release_info = response.json()
        getver = release_info['tag_name']
        current_ver = Version(getver)
        local_filename = 'Skibidi Downloader Installer.exe'
        if current_ver > installed_ver:
            wants_to_update = messagebox.askyesno("Update Available!", f"Would you like to update to {current_ver}?")
            if wants_to_update:
                with requests.get("https://github.com/1333481/SkibidiDownloader/releases/latest/download/Skibidi.Downloader.Installer.exe", stream=True) as r:
                    r.raise_for_status()
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                try:
                    subprocess.Popen([local_filename])
                    os._exit(0)
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error!", "Error opening EXE!")

            else:
                pass
        else:
            pass
    elif system == 'Linux':
        installed_ver = Version("1.0.3")
        response = requests.get("https://api.github.com/repos/1333481/SkibidiDownloader/releases/latest")
        release_info = response.json()
        getver = release_info['tag_name']
        current_ver = Version(getver)
        local_filename = '/usr/local/bin/Skibidi_Downloader'
        if current_ver > installed_ver:
            wants_to_update = messagebox.askyesno("Update Available!", f"Would you like to update to {current_ver}?")
            if wants_to_update:
                with requests.get(f"https://github.com/1333481/SkibidiDownloader/releases/latest/download/Skibidi_Downloader", stream=True) as r:
                    r.raise_for_status()
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                try:
                    subprocess.run(['chmod', '+x', local_filename])
                    subprocess.run([local_filename])
                    os._exit(0)
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error!", "Error running script!")

            else:
                pass
        else:
            pass

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
    error_output = sys.stderr
