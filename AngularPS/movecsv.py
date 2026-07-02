import os
import shutil

# Define the source and destination directories
source_base = "./medelA"
validation_dest = "dataForValidation/modelA"
testing_dest = "dataForTesting/modelA"
learning_dest = "dataForLearning/modelA"

# Ensure destination directories exist
os.makedirs(validation_dest, exist_ok=True)
os.makedirs(testing_dest, exist_ok=True)
os.makedirs(learning_dest, exist_ok=True)

# Function to move CSV files from source to destination
def move_csv_files(start_folder, end_folder, destination):
    for folder_num in range(start_folder, end_folder + 1):
        folder_name = f"{folder_num:03d}"  # Format folder number as 001, 002, etc.
        source_folder = os.path.join(source_base, folder_name)
        
        # Check if source folder exists
        if os.path.exists(source_folder):
            # Iterate through all files in the source folder
            for file_name in os.listdir(source_folder):
                if file_name.endswith(".csv"):  # Check if file is a CSV
                    source_path = os.path.join(source_folder, file_name)
                    dest_path = os.path.join(destination, file_name)
                    
                    # Move the file to the destination
                    shutil.move(source_path, dest_path)
                    print(f"Moved {source_path} to {dest_path}")
        else:
            print(f"Folder {source_folder} does not exist")

# Move files based on folder ranges
move_csv_files(1, 50, validation_dest)   # originalData/001 to 050 -> dataForValidation/meankm
move_csv_files(51, 100, testing_dest)    # originalData/051 to 100 -> dataForTesting/meankm
move_csv_files(101, 500, learning_dest)  # originalData/101 to 500 -> dataForLearning/meankm
print("File moving completed.")