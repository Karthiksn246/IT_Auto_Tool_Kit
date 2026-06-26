import customtkinter as ctk


#Welcome_Page
def load_welcome_page(right_frame):
    welcome_box = ctk.CTkTextbox(
        right_frame,
        font=("Arial", 16),
        wrap="word"
    )
    welcome_box.pack(fill="both", expand=True, padx=20, pady=20)

    welcome_text = """
    Welcome to IT Automation Tool
    
    IT Automation Tool is a comprehensive utility designed to simplify
    day-to-day IT administration tasks through automation and intelligent
    file management.
    
    The application provides a centralized platform for performing common
    operations such as backup, file transfer, folder comparison, duplicate
    file detection, missing file identification, folder size analysis,
    automatic ZIP creation, file organization, and symbolic link creation.
    
    Key Features
    
    • Backup and Restore
    • File Transfer
    • Folder Comparison
    • Folder Size Analyzer
    • Missing File Finder
    • Duplicate File Finder
    • Auto ZIP Creation
    • File Move Automation
    • Soft Link Creation
    • Detailed Log Generation
    
    Select a tool from the left panel to begin.
    """

    welcome_box.insert("1.0", welcome_text)
    welcome_box.configure(state="disabled")


def load_home_page(right_frame):
    # Remove all existing widgets
    for widget in right_frame.winfo_children():
        widget.destroy()

    right_frame.configure(
        fg_color="#EAF4FF"
    )

    load_welcome_page(right_frame)