#!/bin/bash

# Download and run SkibidiDownloader
wget https://github.com/1333481/SkibidiDownloader/releases/latest/download/Skibidi_Downloader.tar.gz -O /tmp/Skibidi_Downloader.tar.gz
tar xf /tmp/Skibidi_Downloader.tar.gz -C /tmp/
cd /tmp/Skibidi_Downloader/
./Skibidi_Downloader.py

