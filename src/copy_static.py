import os
import shutil


def copy_static(source, destination):
    # verify source exists
    if not os.path.exists(source):
        raise ValueError("Source path does not exist")
    for item in os.listdir(source):
        full_path = os.path.join(source, item)
        if os.path.isfile(full_path):
            # Copy file to destination, this is the base case
            print(f"Copying static file {full_path} to {destination}")
            shutil.copy(full_path, destination)
        else:
            # If item is a folder, create it at destination
            new_destination_folder = os.path.join(destination, item)
            os.mkdir(new_destination_folder)
            # Make recursive call on folder item with dest folder you just created
            copy_static(full_path, new_destination_folder)
