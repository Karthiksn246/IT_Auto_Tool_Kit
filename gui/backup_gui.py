import customtkinter as ctk
import threading
from tkinter import filedialog

from modules.backup import BackupEngine
from modules.backup import format_size

engine = None


def browse_source(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0,"end")
        entry.insert(0,folder)

def browse_destination(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0,"end")
        entry.insert(0,folder)


def load_backup_page(right_frame):
    # Remove all existing widgets
    for widget in right_frame.winfo_children():
        widget.destroy()

    right_frame.configure(
        fg_color="#EAF4FF"
    )

    # Header frame
    header_frame = ctk.CTkFrame(
        right_frame,
        fg_color="transparent"
    )
    header_frame.pack(fill="x", padx=10, pady=5)

    title = ctk.CTkLabel(
        header_frame,
        text="Backup",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=0)

    # Backup_Clear_Button
    backup_clear_btn = ctk.CTkButton(
        header_frame,
        text="Clear",
        text_color="black",
        fg_color="lightblue",
        command=lambda: load_backup_page(right_frame),
        width=50
    )
    backup_clear_btn.pack(side="right")

    source_label = ctk.CTkLabel(
        right_frame,
        text="Source Folder :"
    )
    source_label.pack(anchor="w", padx=20)

    source_entry = ctk.CTkEntry(
        right_frame,
        width=500
    )
    source_entry.pack(
        padx=20,
        pady=5
    )

    browse_source_btn = ctk.CTkButton(
        right_frame,
        text="Browse",
        fg_color="purple",
        command=lambda: browse_source(source_entry)
    )
    browse_source_btn.pack(
        padx=20,
        pady=5,
        anchor="w"
    )


    destination_label = ctk.CTkLabel(
        right_frame,
        text="Destination Folder :"
    )
    destination_label.pack(anchor="w", padx=20)

    destination_entry = ctk.CTkEntry(
        right_frame,
        width=500
    )
    destination_entry.pack(
        padx=20,
        pady=5
    )

    browse_destination_btn = ctk.CTkButton(
        right_frame,
        text="Browse",
        fg_color="purple",
        command=lambda: browse_destination(destination_entry)
    )
    browse_destination_btn.pack(
        padx=20,
        pady=5,
        anchor="w"
    )

    start_btn = ctk.CTkButton(
        right_frame,
        text="Start Backup",
        fg_color="purple",
        command=lambda:start_backup_scan(source_entry,destination_entry,status_box,progress,progress_percent,pause_btn,resume_btn,stop_btn))
    start_btn.pack(pady=20)

    progress_text = ctk.CTkLabel(
        right_frame,
        text="Progress"
    )
    progress_text.pack()

    progress = ctk.CTkProgressBar(
        right_frame,
        width=500
    )
    progress.pack()
    progress.set(0)

    progress_percent = ctk.CTkLabel(
        right_frame,
        text="0 %"
    )
    progress_percent.pack()

    status_box = ctk.CTkTextbox(
        right_frame,
        width=600,
        height=150
    )
    status_box.pack(
        pady=10
    )

    control_frame = ctk.CTkFrame(
        right_frame,
        fg_color="transparent"
    )
    control_frame.pack(
        pady=20
    )

    pause_btn = ctk.CTkButton(
        control_frame,
        text="Pause",
        fg_color="orange",
        command=lambda: engine.pause_backup()
    )

    resume_btn = ctk.CTkButton(
        control_frame,
        text="Resume",
        fg_color="green",
        command=lambda: engine.resume_backup()
    )

    stop_btn = ctk.CTkButton(
        control_frame,
        text="Stop",
        fg_color="red",
        command=lambda: engine.stop_backup()
    )


def start_backup_scan(source_entry, destination_entry,status_box,progress,progress_percent, pause_btn,resume_btn, stop_btn):

    source = source_entry.get()
    destination = destination_entry.get()

    global engine

    engine = BackupEngine(source, destination)

    status_box.delete("1.0", "end")
    status_box.insert(
        "end",
        "Scanning Started...\n"
    )
    result = engine.scan_files()

    status_box.insert(
        "end",
        f"""
Scanning Completed

Total Files: {result['total_files']}

Total Size : {format_size(result['total_size'])}

Starting Backup..."""
    )
    # Show buttons first
    pause_btn.pack(side="left", padx=10)
    resume_btn.pack(side="left", padx=10)
    stop_btn.pack(side="left", padx=10)

    # Refresh GUI immediately
    pause_btn.update()
    resume_btn.update()
    stop_btn.update()

    # Then start backup thread
    threading.Thread(
        target=lambda: engine.copy_files(
            progress,
            progress_percent,
            status_box,
        ),
        daemon=True
    ).start()