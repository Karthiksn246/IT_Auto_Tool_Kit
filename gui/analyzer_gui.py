import customtkinter as ctk
import threading
from tkinter import filedialog
from modules.analyzer import FolderAnalyzer

def browse_folder(entry):
    folder = filedialog.askdirectory()
    if folder:
        entry.delete(0,"end")
        entry.insert(0,folder)


def load_analyzer_page(right_frame):
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
        text="Analyzer",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=0)

    # Analyzer_Clear_Button
    analyzer_clear_btn = ctk.CTkButton(
        header_frame,
        text="Clear",
        text_color="black",
        fg_color="lightblue",
        command=lambda: load_analyzer_page(right_frame),
        width=50
    )
    analyzer_clear_btn.pack(side="right")

    target_label = ctk.CTkLabel(
        right_frame,
        text="Target Folder :"
    )
    target_label.pack(anchor="w", padx=20)

    target_entry = ctk.CTkEntry(
        right_frame,
        width=500
    )
    target_entry.pack(
        padx=20,
        pady=5
    )

    browse_target_btn = ctk.CTkButton(
        right_frame,
        text="Browse",
        fg_color="purple",
        command=lambda: browse_folder(target_entry)
    )
    browse_target_btn.pack(
        padx=20,
        pady=5,
        anchor="w"
    )

    start_btn = ctk.CTkButton(
        right_frame,
        text="Start Analyzing",
        fg_color="purple",
        command=lambda: start_folder_scan(
            target_entry,
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
        height=300
    )
    status_box.pack(
        pady=10
    )


#Folder_Scan
def start_folder_scan(
        target_entry,
        status_box,
        progress,
        progress_percent
    ):

    target = target_entry.get()

    analyzer = FolderAnalyzer(
        target ,progress, progress_percent
    )

    status_box.delete(
        "1.0",
        "end"
    )

    status_box.insert(
        "end",
        "Analysis Started...\n"
    )

    threading.Thread(
        target=lambda: run_scan(
            analyzer, status_box
        ),
        daemon=True
    ).start()

def run_scan(analyzer, status_box):
    results = analyzer.scan_folder()
    status_box.after(
        0,
        lambda: status_box.insert(
            "end",
            f"""
Total Subfolders : {results['total_folders']}
Total Files : {results['total_files']}
Hidden Files : {results['hidden_files']}

Log file created...

Analysis Completed!
"""
        )
    )

    status_box.after(
        0,
        status_box.see,
        "end"
    )