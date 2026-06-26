import os
from pathlib import Path
import shutil
from datetime import datetime
import threading

CHUNK_SIZE = 16 * 1024 * 1024  # 16 MB

class BackupEngine:

    def __init__(self, source, destination):

        self.source = Path(source)
        self.destination = Path(destination)

        self.total_files = 0
        self.total_size = 0
        self.processed_bytes =0
        self.file_queue = []
        self.skipped_files = []

        # Control Events
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()

        # Initially running
        self.pause_event.set()

        #copy statistics
        self.copied_files = 0
        self.copied_bytes = 0

        #Time
        self.start_time = None
        self.end_time = None
        self.log_file = None

        #Log File
        self.start_time = datetime.now()
        log_name = self.start_time.strftime(
            "%Y%m%d_%H%M%S.csv"
        )
        self.log_file = Path(
            "logs/Backup"
        ) / log_name

        #Log information
        self.write_log("=" * 60)

        self.write_log("BACKUP LOG")

        self.write_log("=" * 60)

        self.write_log(
            f"Backup Started : {self.start_time}"
        )

        self.write_log(
            f"Source : {self.source}"
        )

        self.write_log(
            f"Destination : {self.destination}"
        )

        self.write_log("")

        self.write_log("-" * 60)
        self.write_log("COPIED FILES")
        self.write_log("-" * 60)

    def scan_files(self):

        self.total_files = 0
        self.total_size = 0
        self.file_queue.clear()

        for root, dirs, files in os.walk(self.source):

            for file in files:

                file_path = Path(root) / file

                try:

                    size = file_path.stat().st_size

                    self.total_files += 1
                    self.total_size += size

                    relative_path = file_path.relative_to(self.source)

                    destination_path = self.destination / relative_path

                    self.file_queue.append(
                        (file_path, destination_path,size)
                    )

                except Exception:
                    continue

        return {

            "total_files": self.total_files,
            "total_size": self.total_size,
            "queue": self.file_queue

        }


    def copy_file(self, source_file, destination_file, progress, progress_percent):

        destination_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(source_file, "rb") as src:

            with open(destination_file, "wb") as dst:

                while True:
                    if self.stop_event.is_set():
                        return

                    self.pause_event.wait()

                    chunk = src.read(CHUNK_SIZE)

                    if not chunk:
                        break

                    dst.write(chunk)

                    self.copied_bytes += len(chunk)

                    self.processed_bytes += len(chunk)

                    percent = self.processed_bytes / self.total_size

                    if self.total_size > 0:
                        percent = self.copied_bytes / self.total_size
                    else:
                        percent = 0

                    progress.after(
                        0,
                        lambda p=percent: progress.set(p)
                    )

                    progress_percent.after(
                        0,
                        lambda p=percent: progress_percent.configure(
                            text=f"{p * 100:.1f}%"
                        )
                    )

        try:
            shutil.copystat(
                source_file,
                destination_file
            )
        except Exception:
            pass

    def copy_files(self, progress, progress_percent, status_box):

        for source_file, destination_file, file_size in self.file_queue:

            if self.stop_event.is_set():
                self.write_log("")
                self.write_log("Backup Stopped By User")
                break

            self.pause_event.wait()

            # Skip if already exists
            if destination_file.exists():
                self.processed_bytes += file_size

                percent = self.processed_bytes / self.total_size

                progress.after(
                    0,
                    lambda p=percent: progress.set(p)
                )

                progress_percent.after(
                    0,
                    lambda p=percent:
                    progress_percent.configure(
                        text=f"{p * 100:.1f}%"
                    )
                )

                self.skipped_files.append(
                    (source_file, destination_file)
                )

                status_box.after(
                    0,
                    lambda s=str(source_file), d=str(destination_file):
                    status_box.insert(
                        "end",
                        f"\nAlready Exists\nSource : {s}\nDestination : {d}\n"
                    )
                )

                status_box.after(
                    0,
                    status_box.see,
                    "end"
                )

                continue

            # Copy file
            self.copy_file(
                source_file,
                destination_file,
                progress,
                progress_percent
            )

            self.write_log(
                str(source_file)
            )

            self.copied_files += 1

            status_box.after(
                0,
                lambda p=str(source_file):
                status_box.insert(
                    "end",
                    f"\nCopied : {p}"
                )
            )

            status_box.after(
                0,
                status_box.see,
                "end"
            )

        if len(self.skipped_files) > 0:

            self.write_log("")
            self.write_log("-" * 60)
            self.write_log("SKIPPED FILES (Already Exists)")
            self.write_log("-" * 60)

            for source_file, destination_file in self.skipped_files:
                self.write_log(
                    f"""
        Source      : {source_file}
        Destination : {destination_file}
        """
                )

        self.end_time = datetime.now()

        total_time = self.end_time - self.start_time

        self.write_log("")
        self.write_log("=" * 60)
        self.write_log("Backup Completed")
        self.write_log(f"End Time : {self.end_time}")
        self.write_log(f"Total Time : {total_time}")
        self.write_log("=" * 60)

        status_box.after(
            0,
            lambda:
            status_box.insert(
                "end",
                "\n\nBackup Completed."
            )
        )

        progress.after(
            0,
            lambda: progress.set(1)
        )

        progress_percent.after(
            0,
            lambda: progress_percent.configure(
                text="100.0%"
            )
        )

    def pause_backup(self):
        self.pause_event.clear()

    def resume_backup(self):
        self.pause_event.set()

    def stop_backup(self):
        self.stop_event.set()

    def write_log(self, text):
        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as log:
             log.write(text + "\n")

def format_size(size):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"