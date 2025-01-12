import os
import sys

def get_data_path(filename, is_resource=False):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS if is_resource else os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if is_resource:
        return os.path.join(base_path, 'templates', filename)
    else:
        temp_data_dir = os.path.join(base_path, 'temp_data')
        os.makedirs(temp_data_dir, exist_ok=True)
        return os.path.join(temp_data_dir, filename)