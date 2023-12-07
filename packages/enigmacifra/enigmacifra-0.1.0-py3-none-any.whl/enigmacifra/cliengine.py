import json
import argparse
from .engine import *
import getpass
from .mshuffle import *
from enigmacifra import __version__
from .defaultRotor import ROTORS

def main():
    parser = argparse.ArgumentParser(description="Enigma-like encryption and decryption tool")
    parser.add_argument('--version', action='version', version=f'Enigma CLI Version: {__version__}', help="Show program's version number and exit")
    subparsers = parser.add_subparsers(dest='command')

    # Add subparsers for the shuffle, encrypt, and decrypt commands
    parser_shuffle = subparsers.add_parser('get-new-rotors', help='Shuffle and create new rotors')
    parser_encrypt = subparsers.add_parser('encrypt', help='Encrypt a message')
    parser_decrypt = subparsers.add_parser('decrypt', help='Decrypt a message')
    args = parser.parse_args()


    if args.command == "get-new-rotors":
        red_start = "\033[91m"
        red_end = "\033[0m"

        # First confirmation
        warning_message = (
            red_start +
            "WARNING: Proceeding will overwrite existing rotor configurations. "
            "This will make previously encrypted data undecipherable unless you "
            "have a backup of the current rotors.\nAre you sure you want to continue? [Y/N]: " +
            red_end
        )
        first_confirm = input(warning_message)

        if first_confirm.lower() == 'y':
            # Second confirmation
            second_confirm = input("Please type 'yes' to confirm: ")
            if second_confirm.lower() == 'yes':
                rotor_file = "defaultRotor.py"
                backup_rotors(rotor_file)
                count = int(input("How many rotors do you want to create? "))
                create_rotors(count)
            else:
                print("Operation cancelled.")
        else:
            print("Operation cancelled.")


    elif args.command in ["encrypt", "decrypt"]:
        # Load the rotor list
        Rotor_lst = ROTORS
        # Prompt for PIN
        pin = getpass.getpass("Enter 8-digit PIN to encrypt/decrypt the password: ")
        pin_confirm = getpass.getpass("Please confirm your PIN: ")
        max_wrong_counts = 1
        while pin_confirm != pin:
            max_wrong_counts += 1
            if max_wrong_counts == 3:
                print("Maximum attempts reached. Exiting.")
                return
            print("----PINs didn't match----")
            pin = getpass.getpass("Enter 8-digit PIN to encrypt/decrypt the password: ")
            pin_confirm = getpass.getpass("Please confirm your PIN: ")
            
        if len(pin) != 8 or not pin.isnumeric():
            print("Invalid PIN. Please enter a 8-digit numeric PIN.")
            return

        PIN = [int(i) for i in pin]
        PEL = Encrypting_package(PIN, Rotor_lst)

        if args.command == "encrypt":
            password = input("Enter the message to be encrypted: ")
            encrypted_message = process_e(PEL, password)
            print("Your encrypted message is: ", encrypted_message)

        elif args.command == "decrypt":
            encrypted_message = input("Enter the encrypted message: ")
            decrypted_message = process_d(PEL, encrypted_message)
            print("Your decrypted message: ", decrypted_message)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
