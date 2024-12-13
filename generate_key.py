import json
from cryptography.fernet import Fernet

key_file = "key"

print("Only run this if you would like to regenerate the key. Doing so will render previous passwords unreadable.")
print("Are you sure you want to continue? y/n")
choice = input().capitalize()
if choice == "Y":
    key = Fernet.generate_key().decode()
    with open(key_file, "w") as outfile:
        outfile.write(key)
    print("Wrote key to file")