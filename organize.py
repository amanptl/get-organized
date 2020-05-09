from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os
import json
import time
import argparse

# Handler that will detect new files.
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        org()

# Organizes by detecting the file types from the file name
def org():
    for file in os.listdir(folder_to_track):
        if os.path.isfile(os.path.join(folder_to_track, file)):
            src = folder_to_track + "/" + file
            for types in generalize:
                if os.path.splitext(file)[1].lower() in generalize[types]:
                    dest = folder_to_track + folders[types]
                    print(file, dest)
                    move_file(src, dest, file)

# Moves the file and creates the sub-directory if it doesn't exist
def move_file(src,dest,file):
    print("Moving file " + file + " to " + dest)
    if not os.path.exists(dest):
        create_dir(dest)
    try:
        shutil.move(src, dest)
    except OSError:
        print("Moving Failed")
    else:
        print("Moved " + file)

# Creates the sub-direcotry
def create_dir(dir):
    try:
        os.mkdir(dir)
    except OSError:
        print (dir + " Creation Failed.")
    else:
        print ("Successfully created the "+ dir + " directory")

# Dictionary of file types based on file extension
generalize = {
    'img' : ('.jpeg', '.jpg', '.png', '.jpg', '.gif', '.raw'),
    'pdf' : ('.pdf'),
    'txt' : ('.txt'),
    'word' : ('.doc', '.docx'),
    'app' : ('.exe', '.lnk')
}

folders = {
    'img' : 'Images',
    'pdf' : 'PDF',
    'txt' : 'Text',
    'word' : 'Word Document',
    'app' : 'Applications'
}

parser = argparse.ArgumentParser(usage="python organize.py <your_directory>")
parser.add_argument('dir', type=str)
args = parser.parse_args()
folder_to_track = args.dir
print("Organizing")
org()
print("Organizing Complete")
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

