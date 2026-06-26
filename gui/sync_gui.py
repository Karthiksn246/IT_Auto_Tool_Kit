import customtkinter as ctk
from tkinter import filedialog
import threading

from modules.sync import FolderSync


def browse_folders(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0,"end")
        entry.insert(0,folder)


def load_sync_page(right_frame):
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
        text="Sync",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=0)

    # Sync_Clear_Button
    sync_clear_btn = ctk.CTkButton(
        header_frame,
        text="Clear",
        text_color="black",
        fg_color="lightblue",
        command=lambda: load_sync_page(right_frame),
        width=50
    )
    sync_clear_btn.pack(side="right")

    folder_a_label = ctk.CTkLabel(
        right_frame,
        text="Folder A :"
    )
    folder_a_label.pack(anchor="w", padx=20)

    folder_a_entry = ctk.CTkEntry(
        right_frame,
        width=500
    )
    folder_a_entry.pack(
        padx=20,
        pady=5
    )

    browse_folder_a_btn = ctk.CTkButton(
        right_frame,
        text="Browse",
        fg_color="purple",
        command=lambda: browse_folders(folder_a_entry)
    )
    browse_folder_a_btn.pack(
        padx=20,
        pady=5,
        anchor="w"
    )

    folder_b_label = ctk.CTkLabel(
        right_frame,
        text="Folder B :"
    )
    folder_b_label.pack(anchor="w", padx=20)

    folder_b_entry = ctk.CTkEntry(
        right_frame,
        width=500
    )
    folder_b_entry.pack(
        padx=20,
        pady=5
    )

    browse_folder_b_btn = ctk.CTkButton(
        right_frame,
        text="Browse",
        fg_color="purple",
        command=lambda: browse_folders(folder_b_entry)
    )
    browse_folder_b_btn.pack(
        padx=20,
        pady=5,
        anchor="w"
    )

    start_btn = ctk.CTkButton(
        right_frame,
        text="Start Syncing",
        fg_color="purple",
        command=lambda: threading.Thread(target=start_sync,
            args=(folder_a_entry,
            folder_b_entry,
            status_box,
            progress,
            progress_percent
        ),daemon=True
        ).start()
    )
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
        height=200
    )
    status_box.pack(
        pady=10
    )


def start_sync(
        folder_a_entry,
        folder_b_entry,
        status_box,
        progress,
        progress_percent
):

    folder_a = folder_a_entry.get().strip()
    folder_b = folder_b_entry.get().strip()

    

    if not folder_a or not folder_b:
        status_box.delete("1.0", "end")
        status_box.insert(
            "end",
            "Please select both folders."
        )
        return

    sync = FolderSync(
        folder_a,
        folder_b,
        progress,
        progress_percent
    )

    status_box.delete("1.0", "end")

    status_box.insert(
        "end",
        "Synchronization Started...\n"
    )

    threading.Thread(
        target=lambda: run_sync(
            sync,
            status_box
        ),
        daemon=True
    ).start()


def run_sync(sync, status_box):

    results = sync.run()

    status_box.after(
        0,
        lambda: status_box.insert(
            "end",
            f"""

Synchronization Completed.

Folder A Files : {results['folder_a_files']}
Folder B Files : {results['folder_b_files']}

Copied to Folder A : {results['copied_to_a']}
Copied to Folder B : {results['copied_to_b']}

Updated Folder A : {results['updated_to_a']}
Updated Folder B : {results['updated_to_b']}

Log Created:

{results['log_file']}
"""
        )
    )

    status_box.after(
        0,
        status_box.see,
        "end"
    )