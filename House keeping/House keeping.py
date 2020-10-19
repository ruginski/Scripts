# Script created to delete temporay files in several folders

import os
import shutil

def fix_path(Folder):
    fixed_path = Folder.replace('\\', '/')
    return fixed_path

def remove_folder_content(Folder):
    print (f"Cleaning folder: {Folder}")

    for filename in os.scandir(Folder):
        file_path = os.path.join(Folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def folder_size(Folder):
    total = 0
    
    for entry in os.scandir(Folder):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)
    return total

def collect_folders():
    base_path = []

    with open("folders.hk") as fp:
        Lines = fp.readlines()
    base_path = [x.rstrip('\n') for x in Lines]

    return base_path

def main():

    base_path = collect_folders()

    for path in base_path:

        fixed_path = fix_path(path)
        print(f"Size of folder '{fixed_path}' before clean up is {folder_size(fixed_path) / 1024 / 1024} MB")
        remove_folder_content(fixed_path)
        print(f"Size of folder '{fixed_path}' after clean up is {folder_size(fixed_path) / 1024 / 1024} MB\n")

if __name__ == "__main__":
    main()