import random
import os
import shutil
import datetime

def randmatch():
    lst = [chr(a) for a in range(33, 126)]
    random.shuffle(lst)
    return dict(zip(lst, lst[::-1]))

def backup_rotors(file_name):
    home_dir = os.path.expanduser("~")
    backup_folder = os.path.join(home_dir, ".enigmabackups")
    original_file_path = file_name
    backup_file_path = os.path.join(backup_folder, os.path.basename(file_name))

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    if os.path.exists(original_file_path):
        backup_path = f"{backup_file_path}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.backup"
        shutil.copy(original_file_path, backup_path)
        print(f"Backup of existing rotors saved as: {backup_path}")

def create_rotors(count):
    # Get the directory of the current script (mshuffle.py)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the file path for defaultRotor.py in the same directory
    file_path = os.path.join(dir_path, 'defaultRotor.py')

    rotors = [randmatch() for _ in range(count)]
    with open(file_path, 'w') as f:
        f.write('ROTORS = ')
        f.write(repr(rotors))
        f.write('\n')

    print(f"New rotors created and saved in: {file_path}")

if __name__ == "__main__":
    rotor_file = 'defaultRotor.py'
    count = int(input('How many rotors do you want to create? '))
    create_rotors(count)
    # create_rotors(rotor_file, count)
