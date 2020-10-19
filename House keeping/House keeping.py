# Script created to clean folder contents

#### THE ACTIONS PERFORMED BY THIS SCRIPT ARE IRREVERSIBLE.
#### USE WITH CAUTION AND BE SURE TO ADD THE CORRECT FOLDERS TO THE folders.hk FILE
#### The author is not responsible for misapplication of this script

#importing necessary libraries
import os #library used to handle some file system activities (scan, folder size)
import shutil #library used to delete folder contents

# folders.hk is a clean text file. Add all the folders that need to be cleaned to it, one folder per line.
# This function will read the folders.hk file and retur the content to the main funcion
def collect_folders():
    base_path = []

    with open("folders.hk") as fp:                                          # buit in Python function used to read the content of a file. Some parameters can be used like 'r'ead and 'w'rite.
        Lines = fp.readlines()                                              # the readlines() iterator will read the file line by line and store the content in Lines variable.
    base_path = [x.rstrip('\n') for x in Lines]                             # the readlines() iterator adds a \n at the end of each line. the rstrip() method is used to remove it from the variable.

    return base_path

# Fuction used to fix the path, so there is no need to worry if the path has / or \, as it will fix the string an ensure that path is in the correct format
def fix_path(Folder):
    fixed_path = Folder.replace('\\', '/')
    
    return fixed_path

# This function will just read the folder size for informational pourposes
def folder_size(Folder):
    total = 0
    
    for entry in os.scandir(Folder):                                        # again using the scandir() to read the folder information
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folder_size(entry.path)

    return total

# Here is where the content of each folder is removed
def remove_folder_content(Folder):
    print (f"Cleaning folder: {Folder}")

    for filename in os.scandir(Folder):                                     # os.scandir() was implemented in modern Python versions. It returns an iterator with all the information from the FS object that it is reading, like name, size and other attribites
        
        file_path = os.path.join(Folder, filename)
        
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):      # checking if the object is a file or simbolic link to call the appropriate "delete" funcion
                os.unlink(file_path)
            elif os.path.isdir(file_path):                                  # checking if the object is a folder to call the appropriate "delete" funcion
                shutil.rmtree(file_path)                                    # using the rmtree() method from the shutil library to recursively delete a directory tree.
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# main function that will call the other functions
def main():
    base_path = collect_folders()

    for path in base_path:
        fixed_path = fix_path(path)
        print(f"Size of folder '{fixed_path}' before clean up is {folder_size(fixed_path) / 1024 / 1024} MB")
        remove_folder_content(fixed_path)
        print(f"Size of folder '{fixed_path}' after clean up is {folder_size(fixed_path) / 1024 / 1024} MB\n")

if __name__ == "__main__":
    main()