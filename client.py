'''
Noah Griffith
CYBR-260-45
Professor Todd Strunce
12/13/2024

Client file for password manager

After the server is started this can be run in its own terminal.
'''

import socket
from cryptography.fernet import Fernet
import json
from prettytable import PrettyTable

host = "127.0.0.1"
port = 56789
passwords = []
key_file = "key"
key = ""

'''
Function: read_key
Purpose: Read the encryption key from a file.
Parameters: None
'''
def read_key():
    try:
        with open(key_file, "r") as outfile:
            return outfile.read()
    except:
        print("Key not found. Please generate a key.")

# Establish initial handshake (not necessary but could be expanded to improve security in the future)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
message = client.recv(1024).decode()
print(f"Waiting for handshake...")
if message == "handshake":
    print('Recieved handshake. Sending ack...')
    client.send("ack".encode())
else:
    print("Handshake not recieved. Closing connection...")
    client.close()

key = read_key()
print(f"Key read: {key}")
cipher = Fernet(key)

while True:
    print("What would you like to do?")
    print("n - New Password")
    print("r - Retrieve Password")
    print("d - Delete Password")
    print("e - Edit Password")
    print("l - Retrieve List")
    print("q - Quit")
    choice = input("> ")

    if choice == "q":
        print("Exiting...")
        client.send("exit".encode())
        break

    elif choice == "n":
        print("Telling the server to create a new password...")
        client.send("new".encode())
        print("What is your new password?")
        password = cipher.encrypt(input().encode())
        client.send(password)
        print("What would you like to associate this new password with? (Username/Website)")
        client.send(input().encode())
        print("=======================================")

    elif choice == "r":
        print("Telling the server to retrieve a password...")
        client.send("retrieve".encode())
        print("What password would you like to retrieve?")
        client.send(input().encode())
        encrypted_password = client.recv(1024).decode()
        try:
            decrypted_password = cipher.decrypt(encrypted_password).decode()
            print(f"That password is {decrypted_password}")
        except:
            print("An error occurred. That password may not exist or the key may be invalid.")
        print("=======================================")

    elif choice == "d":
        print("Telling the server to delete a password...")
        client.send("delete".encode())
        print("What password would you like to delete? Provide user key")
        client.send(input().encode())
        status = client.recv(1024).decode()
        print(f"Status: {status}")
        print("=======================================")

    elif choice == "e":
        print("Telling the server to edit a password...")
        client.send("edit".encode())
        print("What password would you like to edit? Provide user key")
        client.send(input().encode())
        print("What is the new password?")
        password = cipher.encrypt(input().encode())
        client.send(password)
        status = client.recv(1024).decode()
        print(f"Status: {status}")
        print("=======================================")

    elif choice == "l":
        print("Telling the server to retrieve full dictionary...")
        client.send("retrieve_all".encode())
        passwords = json.loads(client.recv(10240).decode())
        table = PrettyTable()
        table.field_names = ["Username", "Password"]
        try:
            for password in passwords:
                table.add_row([password, cipher.decrypt(passwords[password].encode()).decode()])
            print(table)
            print("=======================================")
        except:
            print("Something went wrong. Your key is likely incorrect. Delete any entries made with the old key.")

client.close()
