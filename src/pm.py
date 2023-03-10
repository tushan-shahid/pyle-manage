import hashlib
import os
import time
import tkinter as tk
import shutil
import tkinter.simpledialog as sd
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
import customtkinter

customtkinter.set_appearance_mode("dark")

root = customtkinter.CTk()
root.geometry("1024x900")
root.title("Pyle-Manage")

# colors
bg_textbox = "#8B8B8B"
bg_listbox= "#CDCDC1"


def list_dir():
    listbox.delete(0, tk.END)
    for file in os.listdir(os.getcwd()):
        listbox.insert(tk.END, file)

def on_select(event):
    selected = event.widget.get(event.widget.curselection())
    if os.path.isdir(selected):
        os.chdir(selected)
        entry.delete(0, tk.END)
        entry.insert(tk.END, os.getcwd())
        list_dir()

def go_up():
    os.chdir("..")
    entry.delete(0, tk.END)
    entry.insert(tk.END, os.getcwd())
    list_dir()

def go_to_dir():
    os.chdir(entry.get())
    list_dir()

def create_file():
    with open("new_file.txt", "w") as file:
        file.write("This is a new file.")

    list_dir()

def delete_file():
    selected = listbox.get(listbox.curselection())
    os.remove(selected)
    list_dir()
    
def rename_file():
    selected = listbox.get(listbox.curselection())
    new_name = tk.simpledialog.askstring("Rename File", f"Enter new name for {selected}")
    if new_name:
        os.rename(selected, new_name)
        list_dir()

def create_folder():
    os.mkdir("new_folder")
    list_dir()

def delete_folder():
    selected = listbox.get(listbox.curselection())
    os.rmdir(selected)
    list_dir()

def rename_folder():
    selected = listbox.get(listbox.curselection())
    new_name = tk.simpledialog.askstring("Rename Folder", f"Enter new name for {selected}")
    if new_name:
        os.rename(selected, new_name)
        list_dir()

def on_select(evt):
    """Display tooltip with file information"""
    w = evt.widget
    index = int(w.curselection()[0])
    filename = w.get(index)
    filepath = os.path.join(os.getcwd(), filename)
    created = time.ctime(os.path.getctime(filepath))
    filetype = os.path.splitext(filename)[1]
    filesize = os.path.getsize(filepath)
    tooltip.configure(text=f"Created: {created}\nType: {filetype}\nSize: {filesize}")
    tooltip.place(x=0, y=0, relx=1.0, rely=1.0, anchor='se')
    
    # close tooltip if mouse leaves the listbox
    
    listbox.bind('<Leave>', lambda e: tooltip.place_forget())



def check_for_malware(file_path):
    if os.path.isfile(file_path):
        malicious_hashes = set()
        with open('virushashes.txt', 'r') as f:
            for line in f:
                hash_value = line.strip()
                if hash_value:
                    malicious_hashes.add(hash_value)

        block_size = 65536
        with open(file_path, 'rb') as f:
            hasher = hashlib.md5()
            while True:
                data = f.read(block_size)
                if not data:
                    break
                hasher.update(data)
        file_hash = hasher.hexdigest()
        if file_hash in malicious_hashes:
            return True
        else:
            return False
    else:
        # If it's a folder, return False
        return False

def show_malware():
    file = listbox.get(listbox.curselection())
    text_box.delete("1.0", tk.END)
    if check_for_malware(file):
        text_box.insert(tk.END, f"{file} is infected with malware!")
    else:
        text_box.insert(tk.END, f"{file} is not infected with malware.")




def show_disk_usage():
    """Show disk usage information for the current directory"""
    path = os.path.abspath(os.getcwd())
    total, used, free = shutil.disk_usage(path)
    total_gb = total / 2**30
    used_gb = used / 2**30
    free_gb = free / 2**30
    total_label.configure(text=f"Total: {total_gb:.2f} GB")
    used_label.configure(text=f"Used: {used_gb:.2f} GB")
    free_label.configure(text=f"Free: {free_gb:.2f} GB")
    
def show_directory_structure():
    """Show the current directory structure as an ASCII tree"""
    root_dir = os.getcwd()
    tree = get_directory_tree(root_dir)
    text = "\n".join(tree)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, text)

def get_directory_tree(root_dir):
    """Get the directory structure as an ASCII tree"""
    tree = []
    for path, dirs, files in os.walk(root_dir):
        if path == root_dir:
            dirs = sorted(dirs)
            files = sorted(files)
        else:
            dirs.sort()
            files.sort()
        level = path.replace(root_dir, "").count(os.sep)
        indent = "|   " * (level - 1) + "|-- "
        tree.append(f"{indent}{os.path.basename(path)}/")
        subindent = "|   " * level + "|-- "
        for file in files:
            tree.append(f"{subindent}{file}")
    return tree

def show_bytes():
 # Get the selected file path from the listbox
    selected_item = listbox.curselection()
    if len(selected_item) == 0:
        return
    file_path = listbox.get(selected_item)

    # Read the contents of the file in bytes
    with open(file_path, "rb") as f:
        contents = f.read()

    # Clear the existing contents of the text box and insert the new contents
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, str(contents))
    
# define function to get image metadata
def get_img_meta_data():
    # check if listbox selection is an image file and if so, get the metadata and display it in the text box
    selected_item = listbox.curselection()
    if len(selected_item) == 0:
        return
    file_path = listbox.get(selected_item)
    
    # check if selected file is an image
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            text_box.delete(1.0, tk.END)
            if exif_data:
                meta_data = {}
                for tag_id in exif_data:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exif_data.get(tag_id)
                    if isinstance(data, bytes):
                        data = data.decode()
                    meta_data[tag] = data
                
                # get geo-location metadata
                if 'GPSInfo' in meta_data:
                    gps_info = meta_data['GPSInfo']
                    gps_latitude = gps_info[2] if 2 in gps_info else None
                    gps_latitude_ref = gps_info[1] if 1 in gps_info else None
                    gps_longitude = gps_info[4] if 4 in gps_info else None
                    gps_longitude_ref = gps_info[3] if 3 in gps_info else None

                    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                        # convert geo-location data to decimal degrees
                        latitude = (gps_latitude[0][0] / gps_latitude[0][1] +
                                    gps_latitude[1][0] / gps_latitude[1][1] / 60 +
                                    gps_latitude[2][0] / gps_latitude[2][1] / 3600)
                        if gps_latitude_ref == 'S':
                            latitude = -latitude

                        longitude = (gps_longitude[0][0] / gps_longitude[0][1] +
                                     gps_longitude[1][0] / gps_longitude[1][1] / 60 +
                                     gps_longitude[2][0] / gps_longitude[2][1] / 3600)
                        if gps_longitude_ref == 'W':
                            longitude = -longitude

                        text_box.insert(tk.END, f"Latitude: {latitude:.6f}, Longitude: {longitude:.6f}\n")
                    else:
                        text_box.insert(tk.END, "No geo-location metadata found.\n")
                
                # get image size metadata
                width, height = img.size
                text_box.insert(tk.END, f"Image size: {width}x{height}\n")
                
                # get image pixel metadata
                pixels = img.mode
                text_box.insert(tk.END, f"Image pixels: {pixels}\n")
                
                # get date and time metadata
                if 'DateTimeOriginal' in meta_data:
                    date_time = meta_data['DateTimeOriginal']
                    text_box.insert(tk.END, f"Date taken: {date_time[:10]}\n")
                    text_box.insert(tk.END, f"Time taken: {date_time[11:19]}\n")
                else:
                    text_box.insert(tk.END, "No date and time metadata found.\n")
            else:
                text_box.insert(tk.END, "No metadata found.\n")
    except IOError:
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "Invalid image file.\n")
        
def display_image():
    # check if listbox selection is an image file and if so, display the image in the text_box
    
    selected_item = listbox.curselection()
    if selected_item:
        filename = listbox.get(selected_item[0])
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # create PhotoImage object from image file
            image = Image.open(filename)
            photo = ImageTk.PhotoImage(image)
            # set image of text box
            text_box.image_create('end', image=photo)
            # store reference to PhotoImage object to prevent garbage collection
            text_box.image = photo
    return

def search():
    # ask user for file name to search for
    search_term = sd.askstring("Search", "Enter file name to search for:")    
    # with the search term, search the current directory and match the file name with all the files in the directory in the listbox and highlight the matching file name in the listbox
    if search_term:
        for i in range(listbox.size()):
            if search_term in listbox.get(i):
                listbox.selection_set(i)
                listbox.activate(i)
                break
    return 

def clear_text_box():
    """Clear the text box"""
    text_box.delete("1.0", tk.END)


label = customtkinter.CTkLabel(root, text="Pyle-Manage", font=("Helvetica", 22))
label.pack()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(root,bg=bg_textbox, yscrollcommand=scrollbar.set)
listbox.pack(side="left", fill="both",expand=True)

total_label = customtkinter.CTkLabel(root, font=("Helvetica", 12))
total_label.pack()

used_label = customtkinter.CTkLabel(root, font=("Helvetica", 12))
used_label.pack()

free_label = customtkinter.CTkLabel(root, font=("Helvetica", 12))
free_label.pack()

scrollbar.config(command=listbox.yview)

direction_buttons = customtkinter.CTkFrame(root)
direction_buttons.pack(pady=5)

direction_buttons_label = customtkinter.CTkLabel(direction_buttons, text="Directory Traversal")
direction_buttons_label.pack()

entry = customtkinter.CTkEntry(direction_buttons, width=200)
entry.pack(padx=5, pady=5)

up_button = customtkinter.CTkButton(direction_buttons, text="Previous Directory", command=go_up)
up_button.pack(side="left",padx=5, pady=5)

go_button = customtkinter.CTkButton(direction_buttons, text="Go to Directory", command=go_to_dir)
go_button.pack(side="right",padx=5, pady=5)

file_buttons = customtkinter.CTkFrame(root)
file_buttons.pack(pady=5)

file_buttons2 = customtkinter.CTkFrame(root)
file_buttons2.pack(pady=5)

file_button_label = customtkinter.CTkLabel(file_buttons, text="File Operations")
file_button_label.pack()

create_button = customtkinter.CTkButton(file_buttons, text="Create File", command=create_file)
create_button.pack(side="left",padx=5, pady=5)

delete_button = customtkinter.CTkButton(file_buttons, text="Delete File", command=delete_file)
delete_button.pack(side="left",padx=5, pady=5)

rename_file_button = customtkinter.CTkButton(file_buttons, text="Rename File", command=rename_file)
rename_file_button.pack(padx=5, pady=5)

search_button = customtkinter.CTkButton(file_buttons2, text="Search File", command=search)
search_button.pack(side="left",padx=5, pady=5)

show_content_button = customtkinter.CTkButton(file_buttons2, text='Show file contents in bytes', command=show_bytes)
show_content_button.pack(padx=5, pady=5)

folder_buttons = customtkinter.CTkFrame(root)
folder_buttons.pack(pady=5)

folder_button_label = customtkinter.CTkLabel(folder_buttons, text="Folder Operations")
folder_button_label.pack()

create_folder_button = customtkinter.CTkButton(folder_buttons, text="Create Folder", command=create_folder)
create_folder_button.pack(side="left",padx=5, pady=5)

delete_folder_button = customtkinter.CTkButton(folder_buttons, text="Delete Folder", command=delete_folder)
delete_folder_button.pack(side="left",padx=5, pady=5)

rename_folder_button = customtkinter.CTkButton(folder_buttons, text="Rename Folder", command=rename_folder)
rename_folder_button.pack(side="left",padx=5, pady=5)

dir_tree_button = customtkinter.CTkButton(folder_buttons, text="Show Directory Structure", command=show_directory_structure)
dir_tree_button.pack(padx=5, pady=5)

image_buttons = customtkinter.CTkFrame(root)
image_buttons.pack(pady=5)

extra_buttons = customtkinter.CTkFrame(root)
extra_buttons.pack(pady=5)

image_buttons_label = customtkinter.CTkLabel(image_buttons, text="Image File Operations")
image_buttons_label.pack()

get_meta_data_button = customtkinter.CTkButton(image_buttons, text="Get Img Meta Data", command=get_img_meta_data)
get_meta_data_button.pack(side="left",padx=5, pady=5)

display_image_button = customtkinter.CTkButton(image_buttons, text="Display Image", command=display_image)
display_image_button.pack(padx=5, pady=5)

show_malware_button = customtkinter.CTkButton(extra_buttons, text="Check for Malware", command=show_malware)
show_malware_button.pack(padx=5, pady=5)

clear_button = customtkinter.CTkButton(root, text="Clear ViewBox", command=clear_text_box)
clear_button.pack(side="bottom",padx=5, pady=5)

text_box = tk.Text(root,bg=bg_listbox)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y = tk.Scrollbar(text_box, orient=tk.VERTICAL, command=text_box.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = tk.Scrollbar(text_box, orient=tk.HORIZONTAL, command=text_box.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

text_box.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

show_disk_usage()

list_dir()

listbox.bind('<<ListboxSelect>>', on_select)
tooltip = customtkinter.CTkLabel(root, anchor='w', justify='left')
tooltip.bind('<Enter>', lambda e: tooltip.place_forget())

root.mainloop()
