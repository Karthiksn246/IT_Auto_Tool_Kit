import customtkinter as ctk
import psutil
import os
from gui.backup_gui import load_backup_page
from gui.home import load_welcome_page
from gui.home import load_home_page
from gui.analyzer_gui import load_analyzer_page
from gui.compare_gui import load_compare_page
from gui.sync_gui import load_sync_page
from datetime import datetime
from PIL import Image


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.geometry("1000x800")
app.title("IT Automation Tool Kit")
app.iconbitmap("icons/icon.ico")
old_net = psutil.net_io_counters()
previous_net = psutil.net_io_counters().bytes_recv
previous_disk = psutil.disk_io_counters().read_bytes


#Functions
#DateTime_Def
def update_datetime():
    current = datetime.now().strftime("%A\n----------\n%d-%m-%Y\n%I:%M:%S %p")
    datetime_label.configure(text=current)
    app.after(1000, update_datetime)

#Right_Frame_Clear
def clear_right_frame():
    for widget in right_frame.winfo_children():
        widget.destroy()

#Logs_Open
def open_logs_folder():

    logs_path = os.path.abspath("logs")

    if os.path.exists(logs_path):
        os.startfile(logs_path)

#Update_right_Frame
def update_system_status():
    global previous_net
    global previous_disk

    # CPU
    cpu = psutil.cpu_percent()
    cpu_label.configure(
        text=f"CPU : {cpu}%"
    )
    cpu_bar.set(cpu / 100)

    # RAM
    ram = psutil.virtual_memory().percent
    ram_label.configure(
        text=f"RAM : {ram}%"
    )
    ram_bar.set(ram / 100)

    # Disk Activity
    current_disk = psutil.disk_io_counters().read_bytes
    disk_speed = current_disk - previous_disk
    previous_disk = current_disk

    # Approximate busy %
    disk_percent = min(
        (disk_speed / (50 * 1024 * 1024)) * 100,
        100
    )
    disk_label.configure(
        text=f"Disk : {disk_percent:.0f}%"
    )
    disk_bar.set(
        disk_percent / 100
    )

    app.after(
        1000,
        update_system_status
    )

def update_network_speed():
    global old_net
    new_net = psutil.net_io_counters()
    download_speed = (
        new_net.bytes_recv - old_net.bytes_recv
    ) / 1024 / 1024

    upload_speed = (
        new_net.bytes_sent - old_net.bytes_sent
    ) / 1024 / 1024

    download_label.configure(
        text=f"Download(↓)   : {download_speed:.2f} MB/s"
    )

    upload_label.configure(
        text=f"Upload(↑)         : {upload_speed:.2f} MB/s"
    )

    old_net = new_net

    app.after(
        1000,
        update_network_speed
    )


#Frames
#Header_Frame
header_frame = ctk.CTkFrame(
    app,
    height=80,
    fg_color="#0F172A",   # Header background color
    border_width=0,
    corner_radius=10      # Square corners
)
header_frame.pack(pady=10, padx=5, fill="x")

#Content_Frame
content_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
content_frame.pack(fill="both", expand=True)

#Left_Frame
left_frame = ctk.CTkFrame(
    content_frame,
    width=250,
    fg_color="#1E293B",
    corner_radius=10
)
left_frame.pack(side="left", fill="y", padx=(5, 2.5), pady=5)
left_frame.pack_propagate(False)

#Right_Frame
right_frame = ctk.CTkFrame(
    content_frame,
    fg_color="#F8FAFC",
    corner_radius=10
)
right_frame.pack(side="left", fill="both", expand=True, padx=(2.5, 5), pady=5)


#Header_Logo
logo = ctk.CTkImage(
    light_image=Image.open("icons/logo_rounded.png"),
    size=(200, 60)
)

logo_label = ctk.CTkLabel(
    header_frame,
    image=logo,
    text=''
)
logo_label.place(x=30, rely=0.5, anchor="w")

#DateTime
datetime_label = ctk.CTkLabel(
    header_frame,
    text="",
    font=("Arial", 14),
    text_color="white"
)
datetime_label.place(relx=0.98, rely=0.5, anchor="e")

#Title
header_title = ctk.CTkLabel(
    header_frame,
    text="AUTO TOOL KIT",
    font=("Arial", 28, "bold"),
    text_color = "white"
)
header_title.place(relx=0.5, rely=0.5, anchor="center")

#Home_Button
home_btn = ctk.CTkButton(
    header_frame,
    text="Home",
    fg_color = "#F8FAFC",
    text_color="black",
    command=lambda:load_home_page(right_frame),
    width = 50,
)
home_btn.place(relx=0.70, rely=0.5, anchor="w")

#Logs_Button
logs_btn = ctk.CTkButton(
    header_frame,
    text="Logs",
    width = 50,
    fg_color = "#F8FAFC",
    text_color="black",
    command=open_logs_folder
)
logs_btn.place(relx=0.77, rely=0.5, anchor="w")


#Load_Welcome_Page
load_welcome_page(right_frame)

#Tools_Title
tools = ctk.CTkLabel(
    left_frame,
    text="Select Tool",
    font=("Arial", 20, "bold"),
    text_color = "white"
)
tools.pack(pady=(20,5))


#Buttons_Frame
button_frame = ctk.CTkFrame(
    left_frame,
    fg_color="transparent"
)
button_frame.pack(
    fill="x",
    padx='10',
    pady='10'
)


#Buttons
#Backup_Button
backup_btn = ctk.CTkButton(
    button_frame,
    text="Backup / File Copy",
    command=lambda:load_backup_page(right_frame),
    width = 220
)

#Analyzer_Button
analyzer_btn = ctk.CTkButton(
    button_frame,
    text="Folder Analyzer",
    command=lambda:load_analyzer_page(right_frame),
    width=220
)

#Compare_Button
compare_btn = ctk.CTkButton(
    button_frame,
    text="Compare Folders",
    command=lambda:load_compare_page(right_frame),
    width=220
)

#Synchronic_Button
sync_btn = ctk.CTkButton(
    button_frame,
    text="Sync",
    command=lambda: load_sync_page(right_frame),
    width=220
)

#Recovery_Button
recovery_btn = ctk.CTkButton(
    button_frame,
    text="*Recovery*",
    width=220
)

#Converter_Button
converter_btn = ctk.CTkButton(
    button_frame,
    text="*File Format Converter*",
    width=220
)

#Symlink_Button
symlink_btn = ctk.CTkButton(
    button_frame,
    text="*Symlink*",
    width=220
)

#Cleanup_Button
clean_btn = ctk.CTkButton(
    button_frame,
    text="*Cleanup*",
    width=220
)

backup_btn.grid(row=1, column=0, padx=5, pady=5)

analyzer_btn.grid(row=2, column=0, padx=5, pady=5)

compare_btn.grid(row=3, column=0, padx=5, pady=5)

sync_btn.grid(row=4, column=0, padx=5, pady=5)

recovery_btn.grid(row=5, column=0, padx=5, pady=5)

converter_btn.grid(row=6, column=0, padx=5, pady=5)

symlink_btn.grid(row=7, column=0, padx=5, pady=5)

clean_btn.grid(row=8, column=0, padx=5, pady=5)


#Status Frame
status_frame = ctk.CTkFrame(
    left_frame,
    fg_color="silver"
)
status_frame.pack(fill="x", padx=10, pady=30)

status_title = ctk.CTkLabel(
    status_frame,
    text="System Status",
    font=("Arial", 16, "bold"),
    text_color="Black"
)
status_title.pack(pady=(10,5))

#Cpu
cpu_label = ctk.CTkLabel(
    status_frame,
    text="CPU : 0%",
    text_color="Black"
)
cpu_label.pack(anchor="w", padx=10)

cpu_bar = ctk.CTkProgressBar(
    status_frame,
    width=180
)
cpu_bar.pack(padx=10, pady=(0,10))
cpu_bar.set(0)

#Ram
ram_label = ctk.CTkLabel(
    status_frame,
    text="RAM : 0%",
    text_color="Black"
)
ram_label.pack(anchor="w", padx=10)

ram_bar = ctk.CTkProgressBar(
    status_frame,
    width=180
)
ram_bar.pack(padx=10, pady=(0,10))
ram_bar.set(0)

#Disk
disk_label = ctk.CTkLabel(
    status_frame,
    text="Disk : 0%",
    text_color="Black"
)
disk_label.pack(anchor="w", padx=10)

disk_bar = ctk.CTkProgressBar(
    status_frame,
    width=180
)
disk_bar.pack(padx=10, pady=(0,10))
disk_bar.set(0)

#Download
download_label = ctk.CTkLabel(
    status_frame,
    text="Download : 0 Mbps",
    text_color="Black"
)
download_label.pack(anchor="w", padx=10)

#Upload
upload_label = ctk.CTkLabel(
    status_frame,
    text="Upload : 0 Mbps",
    text_color="Black"
)
upload_label.pack(anchor="w", padx=10, pady=(0,10))



update_network_speed()
update_system_status()
update_datetime()
app.mainloop()