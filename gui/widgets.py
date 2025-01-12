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
        # Upload Section
        upload_frame = ttk.LabelFrame(self, text="Upload CSV File")
        upload_frame.pack(padx=10, pady=10, fill="x") 

        self.upload_button = tk.Button(upload_frame, text="Upload CSV", command=self.upload_file)
        self.upload_button.pack(pady=5)

        # Metadata Section
        metadata_frame = ttk.LabelFrame(self, text="Upload Activity Metadata File")
        metadata_frame.pack(padx=10, pady=10, fill="x")

        self.metadata_button = tk.Button(metadata_frame, text="Upload Metadata CSV", command=self.upload_metadata_file)
        self.metadata_button.pack(pady=5)

        self.metadata_display = tk.Text(metadata_frame, height=10, state=tk.DISABLED)
        self.metadata_display.pack(pady=5)

        # Download Section
        download_frame = ttk.LabelFrame(self, text="Download Results")
        download_frame.pack(padx=10, pady=10, fill="x")

        self.download_button = tk.Button(download_frame, text="Download Assigned Users", command=lambda: self.download_file("temp_data/assigned_users.csv"), state=tk.DISABLED)
        self.download_button.pack(pady=3)

        self.download_button_2 = tk.Button(download_frame, text="Download Unassigned Users", command=lambda: self.download_file("temp_data/unassigned_users.csv"), state=tk.DISABLED)
        self.download_button_2.pack(pady=3)

        self.download_button_3 = tk.Button(download_frame, text="Download Grip Upload", command=lambda: self.download_file("temp_data/grip_upload.csv"), state=tk.DISABLED)
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

            self.create_activity_widgets() 

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

            # Enable the assign button if both data and metadata are uploaded
            if self.data:
                self.assign_button.config(state=tk.NORMAL)

    def create_activity_widgets(self):
        for activity in DataProcessor.activity_cols:
            label = tk.Label(self, text=f"Max capacity for {activity}:")
            label.pack()
            entry = tk.Entry(self)
            entry.pack()
            self.entry_widgets[activity] = entry 
    
    
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
        # Get the base directory (works for both script & executable)
        try:
            if getattr(sys, 'frozen', False):
                base_dir = sys._MEIPASS
            else:   
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            # Construct the full path to the internal file
            internal_filepath = os.path.join(base_dir, filepath)

            # Get the user-selected save location 
            exportfile_path = filedialog.asksaveasfilename(defaultextension=".csv")
            if not exportfile_path:
                return

            # Open the temporary file and the user-specified save location
            with open(internal_filepath, 'r') as infile, open(exportfile_path, 'w', newline='') as outfile:
                csv_reader = csv.reader(infile)
                csv_writer = csv.writer(outfile)
                for row in csv_reader:
                    csv_writer.writerow(row)

        except Exception as e:
            # Handle potential errors (e.g., file not found, permission errors)
            tk.messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

        # try:
        #     with open(filepath, 'r') as infile, open(exportfile_path, 'w', newline='') as outfile:
        #         csv_reader = csv.reader(infile)
        #         csv_writer = csv.writer(outfile)
        #         for row in csv_reader:
        #             csv_writer.writerow(row)

        # except FileNotFoundError:
        #     messagebox.showerror("Error", f"File not found: {filepath}")
        # except Exception as e:
        #     messagebox.showerror("Error", f"An error occurred during download: {e}")                   
    
    # Create a widge to accept user entry in the form of numbers for the maximum activities
    def entry_widgets():
        pass

    """
    If i decide to do different pages this below function should become part of it's own class for that page. TODO: is this a widgets function?
    """
    def on_assign_activity(self):
        DataProcessor.set_data(self.data) 
        max_spaces = self.metadata  # Use metadata for max spaces
        print(max_spaces)
        assignments, unassigned_users = DataProcessor.assign_to_activity(DataProcessor.activity_cols, max_spaces)

        base_path = os.path.dirname(get_data_path("assigned_users.csv"))  # Get the base path
        
        # transform dataframes to csv files
        HandleFiles.write_csv(assignments, "assigned_users.csv", base_path=base_path)
        HandleFiles.write_csv(unassigned_users, "unassigned_users.csv", base_path=base_path)

        # generate the Grip upload csv file:
        HandleFiles.generate_grip_csv(assignments, "grip_upload_template.csv", "grip_upload.csv", base_path=base_path)

        # Delay the ability to donwload files to ensure processing & generating of the activity files in case of large datasets
        time.sleep(2.0)

        #Enable download buttons once the assign activity has been completed
        self.download_button.config(state=tk.NORMAL)
        self.download_button_2.config(state=tk.NORMAL)
        self.download_button_3.config(state=tk.NORMAL)

    class ExportFrame(ttk.Frame):
    # in the future this can be a second page and the download button should be moved here
        pass