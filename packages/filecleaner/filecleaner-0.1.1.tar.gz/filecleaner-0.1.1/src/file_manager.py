
import tkinter as tk

import argparse
from os import listdir
from os.path import isfile
import os, stat
import re
import shutil
import sys




class DirectoryCleaner:
    def __init__(self, directory=f"/Users/{os.getlogin()}/Downloads"):
        self.directory = directory
        self.files = self.get_files()
        self.created_folders = []
        self.errors = []
        self.catagories = ["Images", "Videos", "Audios", "Documents", "Textfiles", "Executable", "Programming", "Special"]
        self.mapping = {
            "jpeg": "Images",
            "png": "Images",
            "mov": "Videos",
            "mp4": "Videos",
            "avi": "Videos",
            "mpg": "Videos",
            "wmv": "Videos",
            "mp3": "Audios",
            "wav": "Audios",
            "mid": "Audios",
            "pptx": "Documents",
            "ppt": "Documents",
            "docx": "Documents",
            "doc": "Documents",
            "xlsx": "Documents",
            "xls": "Documents",
            "csv": "Textfiles",
            "json": "Textfiles",
            "txt": "Textfiles",
            "dmg": "Executable",
            "exe": "Executable",
            "zip": "Special",
            "pdf": "Documents",
            "py": "Programming",
            "html": "Programming",
            "css": "Programming",
            "c": "Programming",
            "java": "Programming",
            "cs": "Programming",
            "PHP": "Programming",
            "swift": "Programming",
            "vb": "Programming",
            "asp": "Programming",
            "xhtml": "Programming",
            "db": "Programming",
            "js": "Programming",
            "md": "Programming",
        }
        

    def get_files(self):
        #create a generator with all files from the given directory
        try:
            file_generator = (file for file in listdir(self.directory) if isfile(f"{self.directory}/{file}"))
        except FileNotFoundError:
            sys.exit("No files found in directory")
        else:
            return file_generator

                        

    def move_files(self):
        #self.files was initialized with the self.get_files() method and includes all files in the directory
        for file in self.files:
            #split text into the filename and the file-extension
            filename, extension = os.path.splitext(f"{self.directory}/{file}")

            #the extension variable include the . in the beginning so through string slicing we can get rid of the dot
            #and see if the exten is included in the self.supported attribute
            if (exten := extension[1:]) in self.mapping:
                #make sure jpg and jpeg are treated as equal
                if exten == "jpg" or exten == "jpeg":
                    exten = "jpeg"

                #exclude error_log.txt because it has to be in the directory
                if file == "error_log.txt":
                    continue
                
                folder_path = f"{self.directory}/{exten}"
                #create folder with the extension as a name
                self.create_folder_if_not_exist(folder_path, exten)
                print(f"{folder_path}    ---    {file}")

                #try to move the given file the newly created folder
                try:
                    os.rename(f"{self.directory}/{file}", f"{folder_path}/{file}")
                except FileNotFoundError:
                    if not os.path.exists(f"{self.directory}/Others"):
                        os.mkdir(f"{self.directory}/Others")
                    #when FileNotFoundError occured move file to Others Folder
                    os.rename(f"{self.directory}/{file}", f"{self.directory}/Others/{file}")
                    #document the error by appending it to the sel.errors attribute
                    self.errors.append(f"FileNotFoundError - {file}\n\n")
            #when the extension is not included in the self.supported attribute do the following
            else:
                if not os.path.exists(f"{self.directory}/Others"):
                    os.mkdir(f"{self.directory}/Others")
                #ty to move the current file to the others Folder
                try:
                    os.rename(f"{self.directory}/{file}", f"{self.directory}/Others/{file}")
                except FileNotFoundError:
                    #document the error by appending it to the sel.errors attribute
                    self.errors.append(f"FileNotFoundError - {file}\n\n")
        

        #this part of the function takes the created folders from above and move them to Folders which further categorize them
        dir_folders = listdir(self.directory)
        for folder in dir_folders:
            if folder == "error_log.txt":
                continue
            if not isfile(folder):
                original_location = f"{self.directory}/{folder}"
                #looking if the folder is in the self.mapping attribute which is a dictionary
                #it maps all potential subfolders (Keys) to a category Folder (Values)
                if folder in self.mapping:
                    #try granting permissions to move the subfolder
                    try:
                        os.chmod(f"{original_location}", stat.S_IRWXU)
                    except PermissionError:
                        self.errors.append(f"PermissionError - {original_location}\n\n")
                        #if there is a PermissionError Skip the folder
                        continue
                    else:
                        #creates the category folder with the self.create_catagory_folder() method using the Value of the given Key
                        self.create_catagory_folder(f"{self.directory}/{self.mapping[folder]}")
                        target_location = f"{self.directory}/{self.mapping[folder]}"
                        #try to move the subfolder with its contents to the category folder
                        try:
                            shutil.move(original_location, target_location)
                        except shutil.Error:
                            self.errors.append(f"shutil.Error - {original_location}\n\n")
                            #When Shutil.Error occurs try to move only the contents of the folder to the category folder
                            files = os.listdir(original_location)
                            for file in files:
                                try:
                                    shutil.move(f"{original_location}/{file}", target_location)
                                except shutil.Error:
                                    self.errors.append(f"shutil.Error - {original_location}\n\n")

                #when folder is not a key in the self.mapping dictionary          
                else:
                    #when the folder is a category folder skip this folder
                    if folder in self.catagories:
                        continue
                    #create a category folder called Others
                    self.create_catagory_folder(f"{self.directory}/Others")
                    target_location = f"{self.directory}/Others"
            
                    #try to move the folder into the Others Category folder
                    try:
                        shutil.move(original_location, target_location)
                    except PermissionError:
                        self.errors.append(f"PermissionError - {original_location}\n\n")
                        #skip when PermissionError is raised
                        continue
                    except shutil.Error:
                        self.errors.append(f"shutil.Error - {original_location}\n\n")
                        #When Shutil.Error occurs try to move only the contents of the folder to the category folder
                        files = os.listdir(original_location)
                        for file in files:
                            try:
                                shutil.move(f"{original_location}/{file}", target_location)
                            except shutil.Error:
                                self.errors.append(f"shutil.Error - {original_location}\n\n")
                            except PermissionError:
                                self.errors.append(f"PermissionError - {original_location}\n\n")
                                
            
            #skip when error_log.txt is the curren file
            else:
                continue

       
            
    #create folder only if the folder doesn't exist and ends with a the extension name       
    def create_folder_if_not_exist(self, path, check):
        if not os.path.exists(path) and path.endswith(check):
            os.mkdir(path)
    
    #create folder only if the folder doesn't exist
    def create_catagory_folder(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    #creates an error-log which includes all paths to files which caused problems during the sorting process
    def create_error_log(self):
        with open("error_log.txt", "w", encoding="utf-8") as errorlog:
            header = "Errorlog"
            errorlog.write(f"\n\n{header.center(35, '*')}")
            errorlog.write("\n\n")
            for line in self.errors:
                errorlog.write(f"{'-' * 50}\n")
                errorlog.write(line)

        os.rename(f"./error_log.txt", f"{self.directory}/error_log.txt")


def  main():
    parser = argparse.ArgumentParser(description="This Automation-Script is sorting files into Folders - Default -> Downloads Directory")
    parser.add_argument("-D", help="Sorting files into Folders in the Desktop Directory", default=False, action="store_true")
    parser.add_argument("-d", help="Sorting files into Folders in the Downloads Directory", default=False, action="store_true")
    
    args = parser.parse_args()          

    if args.D:
        cleanup = DirectoryCleaner(f"/Users/{os.getlogin()}/Desktop")
    elif args.d:
        cleanup = DirectoryCleaner(f"/Users/{os.getlogin()}/Downloads")
    else:
        cleanup = DirectoryCleaner(input("Type in absolute path of the directory that should be sorted: ").strip())


    cleanup.move_files()
    cleanup.create_error_log()



if __name__ == "__main__":
    main()