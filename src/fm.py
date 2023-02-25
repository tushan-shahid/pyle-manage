import os
import time
import tkinter as tk
import shutil
from tkinter import Label, filedialog
import tkinter.simpledialog as sd
from tkinter.tix import IMAGETEXT
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
# import requests

root = tk.Tk()
root.geometry("800x600")
root.title("File Manager")

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
    # api_key="YOUR_API_KEY"
    index = int(w.curselection()[0])
    filename = w.get(index)
    filepath = os.path.join(os.getcwd(), filename)
    created = time.ctime(os.path.getctime(filepath))
    filetype = os.path.splitext(filename)[1]
    filesize = os.path.getsize(filepath)
    # is_malicious = check_for_malware(filepath, api_key)
    tooltip.configure(text=f"Created: {created}\nType: {filetype}\nSize: {filesize}")
    #  bytes\nMalicious: {is_malicious}
    tooltip.place(x=0, y=0, relx=1.0, rely=1.0, anchor='se')
    
    # close tooltip if mouse leaves the listbox
    
    listbox.bind('<Leave>', lambda e: tooltip.place_forget())



# def check_for_malware(filepath, api_key):
#     url = 'https://www.virustotal.com/vtapi/v2/file/scan'
#     files = {'file': (filepath, open(filepath, 'rb'))}
#     params = {'apikey': api_key}
#     response = requests.post(url, files=files, params=params)
#     json_response = response.json()
#     resource = json_response['resource']
#     url = 'https://www.virustotal.com/vtapi/v2/file/report'
#     params = {'apikey': api_key, 'resource': resource}
#     response = requests.get(url, params=params)
#     json_response = response.json()
#     if json_response['response_code'] == 1:
#         if json_response['positives'] > 0:
#             return True
#     return False



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

def clear_text_box():
    """Clear the text box"""
    text_box.delete("1.0", tk.END)


label = tk.Label(root, text="File Manager", font=("Helvetica", 16))
label.pack()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
listbox.pack(side="left", fill="both", expand=True)

total_label = tk.Label(root, font=("Helvetica", 12))
total_label.pack()

used_label = tk.Label(root, font=("Helvetica", 12))
used_label.pack()

free_label = tk.Label(root, font=("Helvetica", 12))
free_label.pack()

scrollbar.config(command=listbox.yview)

up_button = tk.Button(root, text="Up", command=go_up)
up_button.pack()

entry = tk.Entry(root, width=50)
entry.pack()

go_button = tk.Button(root, text="Go", command=go_to_dir)
go_button.pack()

create_button = tk.Button(root, text="Create File", command=create_file)
create_button.pack()

delete_button = tk.Button(root, text="Delete File", command=delete_file)
delete_button.pack()

rename_file_button = tk.Button(root, text="Rename File", command=rename_file)
rename_file_button.pack()

create_folder_button = tk.Button(root, text="Create Folder", command=create_folder)
create_folder_button.pack()

delete_folder_button = tk.Button(root, text="Delete Folder", command=delete_folder)
delete_folder_button.pack()

rename_folder_button = tk.Button(root, text="Rename Folder", command=rename_folder)
rename_folder_button.pack()

dir_tree_button = tk.Button(root, text="Show Directory Structure", command=show_directory_structure)
dir_tree_button.pack()

button = tk.Button(root, text='Show file contents in bytes', command=show_bytes)
button.pack()

get_meta_data_button = tk.Button(root, text="Get Img Meta Data", command=get_img_meta_data)
get_meta_data_button.pack()

display_image_button = tk.Button(root, text="Display Image", command=display_image)
display_image_button.pack()

clear_button = tk.Button(root, text="Clear", command=clear_text_box)
clear_button.pack()

text_box = tk.Text(root)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y = tk.Scrollbar(text_box, orient=tk.VERTICAL, command=text_box.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_x = tk.Scrollbar(text_box, orient=tk.HORIZONTAL, command=text_box.xview)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

text_box.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

show_disk_usage()

list_dir()

listbox.bind('<<ListboxSelect>>', on_select)
tooltip = tk.Label(root, anchor='w', justify='left', bd=1, relief='solid')
tooltip.bind('<Enter>', lambda e: tooltip.place_forget())

root.mainloop()
