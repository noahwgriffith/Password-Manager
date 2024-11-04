import socket
import threading

# This should be read from a configuration file
host = "127.0.0.1"
#host = "raspberrypi"
port = 42069
private_key = ""
passwords = []

def retrieve_all():
    status = "BOF"
    client.send("retrieve_all".encode())
    
    while status != "EOF":
        user = client.recv(1024).decode()
        password = client.recv(1024).decode()
        passwords[user] = password
        status = client.recv(1024).decode()
    return list

def encrypt():
    print("Encrypting...")

# Establish initial handshake
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
        client.send(input().encode())
        print("What would you like to associate this new password with? (Username/Website)")
        client.send(input().encode())

    elif choice == "r":
        print("Telling the server to retrieve a password...")
        client.send("retrieve".encode())
        print("What password would you like to retrieve?")
        client.send(input().encode())
        password = client.recv(1024).decode()
        print(f"That password is {password}")

    elif choice == "d":
        print("Telling the server to delete a password...")
        client.send("delete".encode())
        print("What password would you like to delete? Provide user key")
        client.send(input().encode())
        status = client.recv(1024).decode()
        print(f"Status: {status}")

    elif choice == "e":
        print("Telling the server to edit a password...")
        client.send("edit".encode())
        print("What password would you like to edit? Provide user key")
        client.send(input().encode())
        print("What is the new password?")
        client.send(input().encode())
        status = client.recv(1024).decode()
        print(f"Status: {status}")

    elif choice == "l":
        print("Telling the server to retrieve dictionary...")
        client.send("retrieve_all".encode())
        passwords = retrieve_all()
        print(f"Updated list: {passwords}")

client.close()
