import random
import os
import shutil
import datetime


def randmatch():
    lst = [chr(a) for a in range(33, 126)]
    random.shuffle(lst)
    return dict(zip(lst, lst[::-1]))


import os
import shutil
from datetime import datetime


def backup_default_rotor():
    # Get the current script directory
    script_dir = os.path.dirname(__file__)

    # Define source and destination paths using relative paths
    source_path = os.path.join(script_dir, "..", "enigmacifra", "defaultRotor.py")
    backup_folder = os.path.join(os.path.expanduser("~"), ".enigmabackup")
    backup_path = os.path.join(backup_folder, f"{os.path.basename(source_path)}_{datetime.now().strftime('%Y%m%d%H%M%S')}.backup")

    # Create backup folder if it doesn't exist
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    # Copy the file
    shutil.copy(source_path, backup_path)

    print(f"Backup of defaultRotor.py saved as: {backup_path}")

    # Run the backup function
    



def create_rotors(count):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "defaultRotor.py")
    rotors = [randmatch() for _ in range(count)]
    with open(file_path, "w") as f:
        f.write("ROTORS = ")
        f.write(repr(rotors))
        f.write("\n")
    print(f"New rotors created and saved in: {file_path}")


if __name__ == "__main__":
    rotor_file = "defaultRotor.py"
    backup_default_rotor()
    # create_rotors(rotor_file, count)
