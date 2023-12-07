import json
from enigmacifra.defaultRotor import ROTORS

Rotor_lst = ROTORS


def rotate_single_dict(x, dc):
    """Rotates the given dictionary 'dc' by 'x' positions."""
    dc_rotated = {}
    keys, values = zip(*dc.items())
    for cnt in range(len(dc)):
        dc_rotated[keys[cnt]] = values[(cnt - x) % len(dc)]
    return dc_rotated


def Encrypting_package(pin, rotor_list):
    """Encrypt a package using a PIN and a list of rotors."""
    package_encrypted = []
    for i in range(8):
        pin_digit = pin[i]
        package_encrypted.append(rotate_single_dict(pin_digit, rotor_list[i]))
    return package_encrypted


def passing(pin_encrypted_list, char):
    """Pass a character through the encrypted PIN list to transform it."""
    for rotor in pin_encrypted_list:
        char = rotor[char]
    return char


def get_key_from_value(dc, value):
    """Find the key in a dictionary corresponding to a given value."""
    for key, val in dc.items():
        if val == value:
            return key
    raise ValueError("Value not found in dictionary")


def unpassing(pin_encrypted_list, char):
    """Reverse the transformation process of a character using the encrypted PIN list."""
    for i in range(1, 9):
        char = get_key_from_value(pin_encrypted_list[-i], char)
    return char


"""
Tattoo translates to 'flfvv'. To prevent this repetition, we will update the 'PEL' (Pin Encrypted List) or 'packageE' after every use. This update involves rotating the list by 1 position for each encryption process.
"""


def updating(pin_encrypted_list, encrypt=True):
    """
    Update the PIN Encrypted List (PEL) for encryption or decryption.
    By default, it is set for encryption."""
    direction = 1 if encrypt else -1
    pin = [direction] * 8
    return Encrypting_package(pin, pin_encrypted_list)


def process_e(pin_encrypted_list, password):
    """
    Encrypt a password using the PIN Encrypted List (PEL)."""
    encrypted_password = ""
    for char in password:
        encrypted_password += passing(pin_encrypted_list, char)
        pin_encrypted_list = updating(pin_encrypted_list)
    return encrypted_password


def process_d(PEL, passwordE):
    password = ""
    for str_ in passwordE:
        password += unpassing(PEL, str_)
        PEL = updating(PEL)
    return password


Rotor_lst = ROTORS

"""The above rotor list is to be well backed-up and should never be disturbed as it has contains the shuffled rotors"""
if __name__ == "__main__":
    # Now, We'll ask for the 8-digit PIN

    pin = input("Enter your 8-digit PIN to encrypt/decrypt the password: ")
    if len(pin) == 8 and pin.isnumeric():
        PIN = [int(i) for i in pin]
        PEL = Encrypting_package(PIN, Rotor_lst)
        eVSd = input('Please enter "E" to encrypt or "D" to decrypt: ')
        if eVSd.lower() == "e":
            password = input("Enter the password to be encrypted: ")
            passwordE = process_e(PEL, password)
            print("Your encrypted password is: ", passwordE)
        elif eVSd.lower() == "d":
            passwordE = input("Enter your encrypted passowrd: ")
            password = process_d(PEL, passwordE)
            print("Your decrypted password: ", password)
        else:
            print('Get lost!! I aksed to enter only "E" or "D"')
            print("Thank you for using me!")
    else:
        if pin.isnumeric() == False:
            print("The above is not PIN, Please only enter numbers")
        else:
            if len(pin) == 1:
                print(f"The above PIN is of 1-digit only")
            elif len(pin) < 8:
                print(f"The above PIN is of only {len(pin)}-digits")
            else:
                print(f"The above PIN is of {len(pin)}-digits")
        print("Program ended!")
