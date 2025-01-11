Application Structure

my_csv_app/
├── main.py
├── gui/
│   ├── __init__.py
│   ├── app.py
│   └── widgets.py
├── logic/
│   ├── __init__.py
│   ├── data_processor.py
│   └── file_handler.py
├── assets/
│   └── (optional files like icons, images, etc.)
├── temp_data/
│   ├── (example input CSV files)
│   └── (output CSV files)
└── README.md


- main.py
    This is the entry point for the application, it initialises the main application class and starts the tkinter event loop

- gui
    - app.py
        The main application class that ties everything together. It creates the main window, manages the overall flow, and handles events.
    - widgets.py
       Contains classes for individual GUI components or frames, such as file upload buttons, display areas, etc.

- logic
    - data_processor.py
        Classes to handle and manipulate the data to sort the users into their desired activities
    - file_handler.py
        To handle the reading and writing of the csv file

- assets
    To contain ant optional files like icons, images

- data
    where output and input csv files will be stored
    - utils.py
        potentially somewhere to handle the clean of files for memory as this is all