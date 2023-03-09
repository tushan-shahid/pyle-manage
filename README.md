# Pyle-Manage

Pyle-Manager is a simple file manager application built using Python and the Tkinter library for the UI. It allows users to perform basic file operations such as creating, renaming, and deleting files and folders, as well as viewing file information.

## Installation

- Clone the repository or download the zip file.
- Navigate to the directory where the repository was cloned or the zip file was extracted.
- Install the required dependencies by running the command `pip install -r requirements.txt`.
- Run the command `python extract_hash.py` to extract the malicious hash list from VirusShare.
- Run the command `python pyle_manager.py`.

## Usage

Upon running the application, users will be presented with an interface which includes a list of files and folders in the current directory on the left side. Users can navigate to other directories by typing the path in the text box at the top and pressing the "Go to Directory" button.

Users can perform various file and folder operations using the buttons provided. The "Create File" button creates a new text file, "Create Folder" creates a new directory, and "Delete" and "Rename" buttons delete and rename the selected file or folder, respectively.

When clicking on a file/folder in the left viewbox a detailed information about the selected file or folder, such as its creation date, file type, size, and whether it is malicious or not based on a simple malicious hash check.

There are other fuctions as well try them out.
