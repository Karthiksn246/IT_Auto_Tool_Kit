import os
import shutil
import ctypes

from pathlib import Path
from datetime import datetime

class FolderSync:
    def __init__(self, folder_a, folder_b, progress, progress_percent):
        self.folder_a = Path(folder_a)
        self.folder_b = Path(folder_b)

        self.progress = progress
        self.progress_percent = progress_percent

        self.start_time = datetime.now()

        log_name = self.start_time.strftime("%Y%m%d-%H%M%S")

        self.log_file = (Path("logs/Sync")) / f"{log_name}.txt"

        # Folder Statistics

        self.a_total_files = 0
        self.b_total_files = 0

        self.a_total_folders = 0
        self.b_total_folders = 0

        self.a_hidden_files = 0
        self.b_hidden_files = 0

        self.a_hidden_folders = 0
        self.b_hidden_folders = 0

        self.a_total_size = 0
        self.b_total_size = 0

        # Folder Contents
        self.a_files = {}
        self.b_files = {}

        self.a_folders = set()
        self.b_folders = set()

        # Comparison Results
        self.missing_in_a = []
        self.missing_in_b = []
        self.modified_files = []
        self.missing_folders_in_a = []
        self.missing_folders_in_b = []

        # Sync Results
        self.created_folders = []
        self.copied_to_a = []
        self.copied_to_b = []
        self.updated_to_a = []
        self.updated_to_b = []


    #Hidden_Finder_Func
    def is_hidden(self, path):

        try:

            attrs = ctypes.windll.kernel32.GetFileAttributesW(
                str(path)
            )

            return bool(attrs & 2)

        except:
            return False


    #Format_Size_Func
    def format_size(self, size):

        for unit in ["B", "KB", "MB", "GB", "TB"]:

            if size < 1024:
                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} PB"

    #Log_Write_Fun
    def write_log(self, text):

        self.log_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
                self.log_file,
                "a",
                encoding="utf-8"
        ) as log:
            log.write(text + "\n")

    #Scan
    def scan_folder(self, folder, folder_name):

        files_dict = {}
        folders_set = set()

        total_files = 0
        total_folders = 0
        hidden_files = 0
        hidden_folders = 0
        total_size = 0

        for root, dirs, files in os.walk(folder):

            for dir_name in dirs:

                folder_path = Path(root) / dir_name

                relative_path = str(
                    folder_path.relative_to(folder)
                )

                folders_set.add(relative_path)

                total_folders += 1

                if self.is_hidden(folder_path):
                    hidden_folders += 1

            for file_name in files:

                file_path = Path(root) / file_name

                relative_path = str(
                    file_path.relative_to(folder)
                )

                try:

                    size = file_path.stat().st_size

                    files_dict[relative_path] = size

                    total_files += 1
                    total_size += size

                    if self.is_hidden(file_path):
                        hidden_files += 1

                except:
                    continue

        if folder_name == "A":

            self.a_files = files_dict
            self.a_folders = folders_set

            self.a_total_files = total_files
            self.a_total_folders = total_folders
            self.a_hidden_files = hidden_files
            self.a_hidden_folders = hidden_folders
            self.a_total_size = total_size

            self.progress.after(
                0,
                lambda: self.progress.set(0.25)
            )

            self.progress_percent.after(
                0,
                lambda: self.progress_percent.configure(
                    text="25%"
                )
            )

        else:

            self.b_files = files_dict
            self.b_folders = folders_set

            self.b_total_files = total_files
            self.b_total_folders = total_folders
            self.b_hidden_files = hidden_files
            self.b_hidden_folders = hidden_folders
            self.b_total_size = total_size

            self.progress.after(
                0,
                lambda: self.progress.set(0.50)
            )

            self.progress_percent.after(
                0,
                lambda: self.progress_percent.configure(
                    text="50%"
                )
            )


    #Compare
    def compare(self):

        # Clear previous results
        self.missing_in_a.clear()
        self.missing_in_b.clear()
        self.modified_files.clear()

        self.missing_folders_in_a.clear()
        self.missing_folders_in_b.clear()

        #Missing_Files_in_A
        for file_path in self.b_files:

            if file_path not in self.a_files:
                self.missing_in_a.append(
                    file_path
                )

        # Missing_Files_in_B
        for file_path in self.a_files:

            if file_path not in self.b_files:
                self.missing_in_b.append(
                    file_path
                )

        #Modified_Files
        for file_path in self.a_files:

            if file_path in self.b_files:

                a_file = self.folder_a / file_path
                b_file = self.folder_b / file_path

                try:

                    a_time = a_file.stat().st_mtime
                    b_time = b_file.stat().st_mtime

                    if a_time != b_time:
                        self.modified_files.append(
                            file_path
                        )

                except:
                    continue

        #Missing_Folders_in_A
        for folder in self.b_folders:

            if folder not in self.a_folders:

                self.missing_folders_in_a.append(
                    folder
                )

        #Missing_Folder_in_B
        for folder in self.a_folders:

            if folder not in self.b_folders:
                self.missing_folders_in_b.append(
                    folder
                )

        self.progress.after(
            0,
            lambda: self.progress.set(0.75)
        )

        self.progress_percent.after(
            0,
            lambda: self.progress_percent.configure(
                text="75%"
            )
        )


    #Synchronisation
    def sync(self):
        #Create_Missing_Folders(A)
        for folder in self.missing_folders_in_a:
            destination = self.folder_a / folder

            destination.mkdir(
                parents=True,
                exist_ok=True
            )

            self.created_folders.append(
                str(destination)
            )

        # Create_Missing_Folders(B)
        for folder in self.missing_folders_in_b:
            destination = self.folder_b / folder

            destination.mkdir(
                parents=True,
                exist_ok=True
            )

            self.created_folders.append(
                str(destination)
            )

        #Copy_Missing_in_A
        for file in self.missing_in_a:
            source = self.folder_b / file
            destination = self.folder_a / file

            destination.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            try:

                shutil.copy2(
                    source,
                    destination
                )

                self.copied_to_a.append(file)

            except Exception as e:

                self.write_log(
                    f"Failed to copy {source} -> {destination}"
                )

                self.write_log(str(e))


        #Missing_in_B
        for file in self.missing_in_b:
            source = self.folder_a / file
            destination = self.folder_b / file
            destination.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            try:

                shutil.copy2(
                    source,
                    destination
                )

                self.copied_to_b.append(file)

            except Exception as e:

                self.write_log(
                    f"Failed to copy {source} -> {destination}"
                )

                self.write_log(str(e))

        for file in self.modified_files:

            file_a = self.folder_a / file
            file_b = self.folder_b / file

            try:

                time_a = file_a.stat().st_mtime
                time_b = file_b.stat().st_mtime

                if time_a > time_b:

                    shutil.copy2(
                        file_a,
                        file_b
                    )
                    self.updated_to_b.append(file)

                else:

                    shutil.copy2(
                        file_b,
                        file_a
                    )
                    self.updated_to_a.append(file)

            except Exception as e:

                self.write_log(
                    f"Failed updating {file}"
                )

                self.write_log(str(e))

        self.progress.after(
            0,
            lambda: self.progress.set(1)
        )

        self.progress_percent.after(
            0,
            lambda: self.progress_percent.configure(
                text="100%"
            )
        )


    #Create_Log
    def create_log(self):

        self.write_log("=" * 70)
        self.write_log("FOLDER SYNC LOG")
        self.write_log("=" * 70)

        self.write_log("")
        self.write_log(f"Started : {self.start_time}")
        self.write_log(f"Folder A : {self.folder_a}")
        self.write_log(f"Folder B : {self.folder_b}")

        self.write_log("")
        self.write_log("=" * 70)
        self.write_log("SUMMARY")
        self.write_log("=" * 70)

        self.write_log(
            f"Folder A Files : {self.a_total_files}"
        )

        self.write_log(
            f"Folder B Files : {self.b_total_files}"
        )

        self.write_log(
            f"Folder A Folders : {self.a_total_folders}"
        )

        self.write_log(
            f"Folder B Folders : {self.b_total_folders}"
        )

        self.write_log("")

        self.write_log(
            f"Copied to Folder A : {len(self.copied_to_a)}"
        )

        self.write_log(
            f"Copied to Folder B : {len(self.copied_to_b)}"
        )

        self.write_log(
            f"Folders Created : {len(self.created_folders)}"
        )

        self.write_log(
            f"Updated in Folder A : {len(self.updated_to_a)}"
        )

        self.write_log(
            f"Updated in Folder B : {len(self.updated_to_b)}"
        )

        self.write_log("")


        #Create_Folders
        self.write_log("=" * 70)
        self.write_log("CREATED FOLDERS")
        self.write_log("=" * 70)

        for folder in self.created_folders:
            self.write_log(folder)

        self.write_log("")

        #Files_Copied_to_A
        self.write_log("=" * 70)
        self.write_log("FILES COPIED TO FOLDER A")
        self.write_log("=" * 70)

        for file in self.copied_to_a:
            self.write_log(file)

        self.write_log("")

        #Files_Copied_to_B
        self.write_log("=" * 70)
        self.write_log("FILES COPIED TO FOLDER B")
        self.write_log("=" * 70)

        for file in self.copied_to_b:
            self.write_log(file)

        self.write_log("")

        #Updated_A
        self.write_log("=" * 70)
        self.write_log("UPDATED FILES IN FOLDER A")
        self.write_log("=" * 70)

        for file in self.updated_to_a:
            self.write_log(file)

        self.write_log("")

        #Updated_B
        self.write_log("=" * 70)
        self.write_log("UPDATED FILES IN FOLDER B")
        self.write_log("=" * 70)

        for file in self.updated_to_b:
            self.write_log(file)

        self.write_log("")

        end_time = datetime.now()

        self.write_log("")
        self.write_log("=" * 70)

        self.write_log(
            f"Completed : {end_time}"
        )

        self.write_log(
            f"Duration : {end_time - self.start_time}"
        )

        self.write_log("=" * 70)

    def run(self):

        self.scan_folder(
            self.folder_a,
            "A"
        )

        self.scan_folder(
            self.folder_b,
            "B"
        )

        self.compare()

        self.sync()

        self.create_log()

        return {

            "folder_a_files": self.a_total_files,
            "folder_b_files": self.b_total_files,

            "copied_to_a": len(
                self.copied_to_a
            ),

            "copied_to_b": len(
                self.copied_to_b
            ),

            "updated_to_a": len(
                self.updated_to_a
            ),

            "updated_to_b": len(
                self.updated_to_b
            ),

            "log_file": self.log_file

        }