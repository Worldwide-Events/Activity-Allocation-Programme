# main app page where the app will run from and contain classes to handle the flow
import tkinter as tk
from gui.widgets import UploadFrame

# class to initialse our main window and run our application
class ActivityApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('WWE Activity Sorter')
        self.upload_frame = UploadFrame(self.root)
        

    # method to run the application
    def run(self):
        self.root.mainloop()