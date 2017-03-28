#!/usr/bin/env python

##################################################################
# This is a script that runs on the door unlocking hardware 
# that's designed to reset Connor's walk-in music whenever he
# tries to change it.  It selects a random mp3 from the specified
# directory and copies it on top of Connor's change.
#
# I'm obscuring some of the filepaths and extensions here to make
# it a bit harder for him to search the filesystem for this stuff.
##################################################################

import gamin
import time
import random
from os import path
from os import listdir
from shutil import copyfile

MEDIA_FILE_PATH = "/opt/.raspi_gpio/media/"
MEDIA_FILE_EXTENSION = ".meh"
TARGET_FILE_NAME = "connor.mp3"
TARGET_FILE_DIR = "/media/AMD/WALKON/"

def is_a_hidden_mp3_file(filepath) :
    if path.isfile(filepath) == 0:
        return 0
    extension = path.splitext(filepath)[1]
    return (extension == MEDIA_FILE_EXTENSION)

def get_hidden_mp3_files(dir):
    return [path.join(dir, f) for f in listdir(dir) if is_a_hidden_mp3_file(path.join(dir, f))]

def choose_new_file():
    files = get_hidden_mp3_files(MEDIA_FILE_PATH)
    return random.choice(files)

def on_directory_changed(path, event):
    if (event >= 8):     # can't actually find docs for gamin's python bindings
        return           # but the event nums for file changes appear to be <8 ish.

    if TARGET_FILE_NAME not in path:
        return

    copyfile(choose_new_file(), TARGET_FILE_DIR + TARGET_FILE_NAME)

mon = gamin.WatchMonitor()
mon.watch_directory(TARGET_FILE_DIR, on_directory_changed)
while(1):
    time.sleep(10)
    ret = mon.handle_events()