import customtkinter as ctk
from tkinter import filedialog
import threading
from modules.compare import FolderCompare

def browse_folders(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0,"end")
        entry.insert(0,folder)


def load_compare_page(right_frame):
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
        text="Compare",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=0)

    # Compare_Clear_Button
    compare_clear_btn = ctk.CTkButton(
        header_frame,
        text="Clear",
        text_color="black",
        fg_color="lightblue",
        command=lambda: load_compare_page(right_frame),
        width=50
    )
    compare_clear_btn.pack(side="right")

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
        text="Start Comparison",
        fg_color="purple",
        command=lambda: start_comparison(
            folder_a_entry,
            folder_b_entry,
            status_box,
            progress,
            progress_percent
        )
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

def start_comparison(
        folder_a_entry,
        folder_b_entry,
        status_box,
        progress,
        progress_percent
):
    folder_a = folder_a_entry.get()
    folder_b = folder_b_entry.get()

    status_box.delete(
        "1.0",
        "end"
    )

    status_box.insert(
        "end",
        "Comparison Started...\n"
    )

    threading.Thread(
        target=lambda: run_compare(
            folder_a,
            folder_b,
            status_box,
            progress,
            progress_percent
        ),
        daemon=True
    ).start()

def run_compare(
        folder_a,
        folder_b,
        status_box,
        progress,
        progress_percent
):

    compare = FolderCompare(
        folder_a,
        folder_b,
        progress,
        progress_percent
    )

    report_file = compare.run()

    status_box.after(
        0,
        lambda: status_box.insert(
            "end",
            f"""

Excel Report Created

{report_file}

Comparison Completed
"""
        )
    )
