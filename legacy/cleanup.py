'''
Removes duplicate images from a folder, storing them into another. 
Duplicates are determined as files which have brackets in their name.
If one file is left, it is spared. 
Mainly used as a utility function for the old image training dataset.
'''

import os
import re
import shutil

def move_files_without_brackets(source_folder, destination_folder):
    """
    Moves files from a source folder to a destination folder if the filename doesn't contain brackets.

    Args:
        source_folder: Path to the source folder.
        destination_folder: Path to the destination folder.  Will be created if it doesn't exist.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for root, _, files in os.walk(source_folder):
        for file in files:
            if re.search(r'[\(\)]', file):  # Check for brackets in filename
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_folder, file)
                try:
                    if len(os.listdir(root)) != 1:
                        shutil.move(source_path, destination_path)
                        print(f"Moved '{file}' to '{destination_folder}'")
                except Exception as e:
                    print(f"Error moving '{file}': {e}")

def check_for_empty_folders(folder):
    # for each_folder in os.listdir(folder):
    #     print(each_folder)
    for root, _, files in os.walk(folder):
        if len(files) == 0:
            print(f"Folder '{root}' is empty")

move_files_without_brackets('./training - Copy', './cleaned')
check_for_empty_folders('./training - Copy')