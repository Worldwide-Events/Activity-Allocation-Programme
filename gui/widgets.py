import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from logic.file_handler import HandleFiles
from logic.data_processor import *
from gui.utils import get_data_path
import csv
import os
import sys
import time

# Class for frame to set up the activites and the numbers for each activity
class ActivityFrame(ttk.Frame):
    pass


# Class for frame to upload file
class UploadFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.entry_widgets = {}
        self.data = None
        self.metadata = None  # Add attribute to store metadata

        self.container.geometry('550x500+500+400')

        # Create a style object to manage colors
        self.style = ttk.Style()

        # Configure colors for light mode
        self.style.configure("TFrame", background="white")
        self.style.configure("TLabel", background="white", foreground="black")
        self.style.configure("TButton", background="#4CAF50", foreground="white") 

        # Detect dark mode and adjust colors if necessary
        dark_mode_themes = ["azure-dark", "darkaqua"]  # Add more theme names as needed
        if self.container.tk.call("ttk::style", "theme", "use") in dark_mode_themes:
            self.style.configure("TFrame", background="black")
            self.style.configure("TLabel", background="black", foreground="white")
            self.style.configure("TButton", background="#2E8B57", foreground="white") 

    def create_widgets(self):
        # Metadata Section
        metadata_frame = ttk.LabelFrame(self, text="Step 1: Upload Activity Metadata File")
        metadata_frame.pack(padx=10, pady=10, fill="x")

        self.metadata_button = tk.Button(metadata_frame, text="Upload Metadata CSV", command=self.upload_metadata_file)
        self.metadata_button.pack(pady=5)

        self.metadata_display = tk.Text(metadata_frame, height=10, state=tk.DISABLED)
        self.metadata_display.pack(pady=5)

        # Upload Section
        upload_frame = ttk.LabelFrame(self, text="Step 2: Upload Attendee CSV File")
        upload_frame.pack(padx=10, pady=10, fill="x") 

        self.upload_button = tk.Button(upload_frame, text="Upload CSV", command=self.upload_file, state=tk.DISABLED)
        self.upload_button.pack(pady=5)

        # Download Section
        download_frame = ttk.LabelFrame(self, text="Download Results")
        download_frame.pack(padx=10, pady=10, fill="x")

        self.download_button = tk.Button(download_frame, text="Download Assigned Users", command=lambda: self.download_file("gui/temp_data/assigned_users.csv"), state=tk.DISABLED)
        self.download_button.pack(pady=3)

        self.download_button_2 = tk.Button(download_frame, text="Download Unassigned Users", command=lambda: self.download_file("gui/temp_data/unassigned_users.csv"), state=tk.DISABLED)
        self.download_button_2.pack(pady=3)

        self.download_button_3 = tk.Button(download_frame, text="Download Grip Upload", command=lambda: self.download_file("gui/temp_data/grip_upload.csv"), state=tk.DISABLED)
        self.download_button_3.pack(pady=3)

        # Assign Button
        self.assign_button = tk.Button(self, text="Assign Activities", command=self.on_assign_activity, state=tk.DISABLED)
        self.assign_button.pack(pady=10)

    def upload_file(self):
        # Open a file dialog to select a CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            # Call the function from file_handler to read the CSV
            data = HandleFiles.read_csv(file_path)
            self.data = data # store the data in a class attribute
            DataProcessor.set_data(data)

            # Enable the assign button if both data and metadata are uploaded
            if self.metadata:
                self.assign_button.config(state=tk.NORMAL)

    def upload_metadata_file(self):
        # Open a file dialog to select a CSV file
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            # Read the metadata CSV file
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                self.metadata = {row['Activity']: int(row['Spaces']) for row in reader}

            # Display the metadata in the text widget
            self.metadata_display.config(state=tk.NORMAL)
            self.metadata_display.delete(1.0, tk.END)
            for activity, spaces in self.metadata.items():
                self.metadata_display.insert(tk.END, f"{activity}: {spaces} spaces\n")
            self.metadata_display.config(state=tk.DISABLED)

            # Enable the upload button if metadata is uploaded
            if self.metadata:
                self.upload_button.config(state=tk.NORMAL)

            # Enable the assign button if both data and metadata are uploaded
            if self.data:
                self.assign_button.config(state=tk.NORMAL)

    def create_activity_widgets(self):
        self.metadata_display.config(state=tk.NORMAL)
        self.metadata_display.delete(1.0, tk.END)
        for activity, spaces in self.metadata.items():
            self.metadata_display.insert(tk.END, f"{activity}: {spaces} spaces\n")
        self.metadata_display.config(state=tk.DISABLED)
    
    
    # # this is to be moved to export frame in the future once multiple pages have been established
    # def download_file(self, filepath):
    #     exportfile_path = filedialog.asksaveasfilename(defaultextension=".csv")
    #     if not exportfile_path:  # User cancelled the save dialog
    #         return
    #     with open(filepath, 'r') as infile, open(exportfile_path, 'w', newline='') as outfile:
    #             csv_reader = csv.reader(infile)
    #             csv_writer = csv.writer(outfile)
    #             for row in csv_reader:
    #                 csv_writer.writerow(row)

    """
    Downloads a csv file to a user specified location
    Args:
        filepath (str):  The relative path to the csv file within the application
    """
    def download_file(self, filepath):
        try:
            # Get filename from filepath
            filename = os.path.basename(filepath)
            source_path = get_data_path(filename)
            
            # Get save location from user
            export_path = filedialog.asksaveasfilename(defaultextension=".csv")
            if not export_path:  # User cancelled
                return
                
            # Copy file contents
            with open(source_path, 'r') as infile, open(export_path, 'w', newline='') as outfile:
                csv_reader = csv.reader(infile)
                csv_writer = csv.writer(outfile)
                for row in csv_reader:
                    csv_writer.writerow(row)

        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

    """
    If i decide to do different pages this below function should become part of it's own class for that page. TODO: is this a widgets function?
    """
    def on_assign_activity(self):
        DataProcessor.set_data(self.data) 
        max_spaces = self.metadata  # Use metadata for max spaces
        print(max_spaces)
        assignments, unassigned_users = DataProcessor.assign_to_activity(max_spaces)

        #base_path = os.path.dirname(get_data_path("assigned_users.csv"))  # Get the base path
        base_path = os.path.dirname(get_data_path("")) # Use the utility function to get the base path
        
        # transform dataframes to csv files
        HandleFiles.write_csv(assignments, "assigned_users.csv")
        HandleFiles.write_csv(unassigned_users, "unassigned_users.csv")

        # generate the Grip upload csv file:
        template_path = get_data_path("grip_upload_template.csv", is_resource=True)
        print(template_path)
        HandleFiles.generate_grip_csv(assignments, template_path, "grip_upload.csv")

        # Delay the ability to download files to ensure processing & generating of the activity files in case of large datasets
        time.sleep(2.0)

        # Enable download buttons once the assign activity has been completed
        self.download_button.config(state=tk.NORMAL)
        self.download_button_2.config(state=tk.NORMAL)
        self.download_button_3.config(state=tk.NORMAL)

        # Clear data after processing
        DataProcessor.clear_data()
        # HandleFiles.clear_data()

    class ExportFrame(ttk.Frame):
    # in the future this can be a second page and the download button should be moved here
        pass