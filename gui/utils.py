import os
import sys

# def get_data_path(filename):
#     if getattr(sys, 'frozen', False):
#         # If the application is run as a bundle, the PyInstaller bootloader
#         # extends the sys module by a flag frozen=True and sets the app 
#         # path into variable _MEIPASS'.
#         application_path = sys._MEIPASS
#     else:
#         application_path = os.path.dirname(os.path.abspath(__file__))

#     return os.path.join(application_path, filename)

def get_data_path(filename):
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path, including 'temp_data'
    full_path = os.path.join(application_path, 'temp_data', filename)

    # Create 'temp_data' directory if it doesn't exist
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    return full_path