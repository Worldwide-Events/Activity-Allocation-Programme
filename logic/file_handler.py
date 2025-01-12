# Class to handle files being imported 

"""
A user can import a file
The file then needs to be stored in memory in the data section
"""

# import statements
import pandas as pd
import csv
import os
from gui.utils import get_data_path

# if the file upload functionality is a widget do I really need a file handler.py?


class HandleFiles:
    def __init__(self, file_name):
        self.file_name = file_name

# function to read the csv files as a data frame to then be able to use later on
# TODO: This needs to be changed to read the file that get's uploaded
    def read_csv(file_name): 
        try:
            df = pd.read_csv(file_name)
            return df
        
        #TODO: Improve error handling
        except Exception as e:
            print(f"Error reading {file_name}: {e}")


# function to save data as a csv file - tbc on if it will need updating later on
    @staticmethod
    def write_csv(data, output_file): 
        try:
            output_path = get_data_path(output_file)
            data.to_csv(output_path, index=False)
        except Exception as e: 
            print(f"Error writing to {output_path}: {e}")


# function to generate the grip upload
    #TODO: spend some time understanding the one liner
    def generate_grip_csv(df, input_file, output_file):
        activity_to_gripids = df.groupby('Assigned Activity')['Attendee ID'].apply(lambda x: ' | '.join(x.astype(str))).to_dict()

        try:
            input_file = get_data_path(input_file)
            output_file = get_data_path(output_file)

            # Ensure the directory for output_file exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            print(f"Input file path: {input_file}")  # Print the input file path
            print(f"Output file path: {output_file}")  # Print the output file path

            # read the first two rows to save for the output and the header
            with open(input_file, "r", newline='') as infile, \
                open(output_file, "w", newline='') as outfile:
                
                reader = csv.reader(infile)
                writer = csv.writer(outfile)

                first_two_rows = [next(reader) for _ in range(2)]
                header = next(reader)
                writer.writerows(first_two_rows)
                writer.writerow(header)

                # get the indices of the columns we need to write out to
                key_column_index = header.index("Session Name en-gb *")
                value_column_index = header.index("Attendee ID")

                print(f"key_column_index: {key_column_index}")  # Print the key column index
                print(f"value_column_index: {value_column_index}")  # Print the value column index

                # Write the dictionary data to the specified columns
                for key, value in activity_to_gripids.items():
                    row = [""] * len(header)  # Create an empty row
                    row[key_column_index] = key
                    row[value_column_index] = value
                    writer.writerow(row)
        
        # except FileNotFoundError:
        #     print(f"Error: The file template file was not found.")
        # except ValueError:
        #     print(f"Error: Column names 'Session Name en-gb *' or 'Attendee ID' not found in the CSV header.")
        # except Exception as e:
        #     print(f"An error occurred: {e}")

        except FileNotFoundError:
            print(f"Error: The file '{input_file}' was not found.")
        except ValueError as e:
            print(f"Error: {e}")  # Print the specific ValueError message
        except Exception as e:
            print(f"An error occurred: {e}")
