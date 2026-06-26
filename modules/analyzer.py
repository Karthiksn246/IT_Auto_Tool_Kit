import os
import ctypes
from pathlib import Path
from datetime import datetime


#Analyzer_Class
class FolderAnalyzer:

    def __init__(self, target, progress, progress_percent):

        self.target = Path(target)

        self.progress = progress
        self.progress_percent = progress_percent

        self.total_files = 0
        self.total_folders = 0
        self.hidden_files = 0
        self.total_size = 0

        self.file_types = {}
        self.folder_sizes = {}

        self.folder_details = []
        self.file_details = []
        self.hidden_file_details = []

        self.start_time = datetime.now()

        log_name = self.start_time.strftime(
            "%Y%m%d_%H%M%S.txt"
        )

        self.log_file = Path(
            "logs/Analyzer"
        ) / log_name

    def is_hidden(self, path):

        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(
                str(path)
            )

            return bool(attrs & 2)

        except:
            return False

    def format_size(self, size):

        for unit in ["B", "KB", "MB", "GB", "TB"]:

            if size < 1024:
                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} PB"

    def write_log(self, text):

        with open(
                self.log_file,
                "a",
                encoding="utf-8"
        ) as log:

            log.write(text + "\n")

    def scan_folder(self):
        total_items = 0

        for root, dirs, files in os.walk(self.target):
            total_items += len(dirs) + len(files)

        processed_items = 0

        for root, dirs, files in os.walk(self.target):
            for folder in dirs:

                processed_items += 1

                if total_items > 0:
                    percent = processed_items / total_items

                    self.progress.after(
                        0,
                        lambda p=percent:
                        self.progress.set(p)
                    )

                    self.progress_percent.after(
                        0,
                        lambda p=percent:
                        self.progress_percent.configure(
                            text=f"{p * 100:.1f}%"
                        )
                    )

            self.total_folders += len(dirs)

            for file in files:
                processed_items += 1

                if processed_items % 500 == 0 and total_items > 0:
                    percent = processed_items / total_items

                    self.progress.after(
                        0,
                        lambda p=percent:
                        self.progress.set(p)
                    )

                    self.progress_percent.after(
                        0,
                        lambda p=percent:
                        self.progress_percent.configure(
                            text=f"{p * 100:.1f}%"
                        )
                    )

                file_path = Path(root) / file

                try:

                    size = file_path.stat().st_size

                    self.total_files += 1
                    self.total_size += size

                    parent = Path(root)

                    while parent != self.target.parent:

                        parent_str = str(parent)

                        self.folder_sizes[parent_str] = (
                                self.folder_sizes.get(parent_str, 0)
                                + size
                        )

                        if parent == self.target:
                            break

                        parent = parent.parent

                    self.file_details.append(
                        (file_path, size)
                    )

                    extension = (
                        file_path.suffix.lower()
                        .replace(".", "")
                    )

                    if extension == "":
                        extension = "no_extension"

                    self.file_types[extension] = (
                        self.file_types.get(
                            extension,
                            0
                        ) + 1
                    )

                    if self.is_hidden(file_path):

                        self.hidden_files += 1

                        self.hidden_file_details.append(
                            (file_path, size)
                        )

                except Exception:
                    continue

        for folder_path, folder_size in sorted(
                self.folder_sizes.items()
        ):
            self.folder_details.append(
                (
                    Path(folder_path),
                    folder_size
                )
            )

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

        self.create_log()

        return {

            "total_folders": self.total_folders,
            "total_files": self.total_files,
            "hidden_files": self.hidden_files,
            "total_size": self.total_size,
            "file_types": self.file_types

        }

    def create_log(self):

        self.write_log("=" * 60)
        self.write_log("FOLDER ANALYZER LOG")
        self.write_log("=" * 60)
        self.write_log("")

        self.write_log(
            f"Analysis Started : {self.start_time}"
        )

        self.write_log(
            f"Target Folder : {self.target}"
        )

        self.write_log("")

        self.write_log("=" * 60)
        self.write_log("SUMMARY")
        self.write_log("=" * 60)

        self.write_log(
            f"Total Subfolders : {self.total_folders}"
        )

        self.write_log(
            f"Total Files : {self.total_files}"
        )

        self.write_log(
            f"Hidden Files : {self.hidden_files}"
        )

        self.write_log(
            f"Total Size : {self.format_size(self.total_size)}"
        )

        self.write_log("")

        self.write_log("=" * 60)
        self.write_log("FILE TYPES")
        self.write_log("=" * 60)

        for ext, count in sorted(
                self.file_types.items()
        ):

            self.write_log(
                f"{ext} : {count}"
            )

        self.write_log("")
        self.write_log("=" * 60)
        self.write_log("SUBFOLDERS")
        self.write_log("=" * 60)

        for folder, size in self.folder_details:

            self.write_log(
                f"\n{folder}"
            )

            self.write_log(
                f"Size : {self.format_size(size)}"
            )

        self.write_log("")
        self.write_log("=" * 60)
        self.write_log("FILES")
        self.write_log("=" * 60)

        for file_path, size in self.file_details:

            self.write_log(
                f"\n{file_path}"
            )

            self.write_log(
                f"Size : {self.format_size(size)}"
            )

        self.write_log("")
        self.write_log("=" * 60)
        self.write_log("HIDDEN FILES")
        self.write_log("=" * 60)

        for file_path, size in self.hidden_file_details:

            self.write_log(
                f"\n{file_path}"
            )

            self.write_log(
                f"Size : {self.format_size(size)}"
            )

        end_time = datetime.now()

        total_time = (
                end_time -
                self.start_time
        )

        self.write_log("")
        self.write_log("=" * 60)

        self.write_log(
            "Analysis Completed"
        )

        self.write_log(
            f"End Time : {end_time}"
        )

        self.write_log(
            f"Total Time : {total_time}"
        )

        self.write_log("=" * 60)