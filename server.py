import socket
import threading
import json

# This should be read from a configuration file
host = "127.0.0.1"
port = 42069
list_file = "list.json"

def write_list(passwords):
    print("Saving list...")
    with open(list_file, "w") as outfile:
        json.dump(passwords, outfile)
    print("List saved")

def read_list():
    print("Reading list...")
    with open(list_file, "r") as outfile:
        passwords = json.load(outfile)
    print("List read")
    return passwords

# Load passwords from file
passwords = read_list()

def new_password(user, password):
    print(f"Writing entry for {user}:{password} to disk...")
    write_list(passwords)

def retrieve_password(user):
    print(f"Retriving entry for {user}...")
    write_list(passwords)
    return passwords[user]

def retrieve_all():
    print("Fetching list!")

def delete_password(user):
    print(f"Deleting entry for {user}...")
    if passwords.pop(user, None) == None:
        print(f"No entry for {user}. Returning None.")
        return None
    else:
        write_list(passwords)
        return "SUCCESS"

def edit_password(user, password):
    print(f"Updating entry for {user} with new password {password}...")
    if user in passwords:
        print(f"Found entry for {user}...")
        passwords[user] = password
        print(f"Updated password.")
        write_list(passwords)
        return "SUCCESS"
    else:
        return None


def handle_request(request, client):

    if request == "new":
        print("Making a new password!")
        password = client.recv(1024).decode()
        print(f"Client sent {password}")
        user = client.recv(1024).decode()
        print(f"Client sent {user}")
        passwords[user] = password
        new_password(user, password)
        write_list(passwords)

    elif request == "retrieve":
        print("Retrieving a password!")
        user = client.recv(1024).decode()
        try:
            print(f"Client asked for the password at {user}")
            client.send(retrieve_password(user).encode())
        except:
            print("Failed to retrieve password, sending error")
            client.send("ERROR".encode())

    elif request == "retrieve_all":
        retrieve_all()

    elif request == "delete":
        print("Deleting a password!")
        user = client.recv(1024).decode()
        print(f"Client asked to delete password at {user}")
        status = delete_password(user)
        if status == None:
            print("Returned None. Alerting client.")
            client.send("ERROR".encode())
        else:
            print(f"Deleted password for {user}. Alerting client.")
            client.send(status.encode())

    elif request == "edit":
        print("Editing a password!")
        user = client.recv(1024).decode()
        print(f"Client asked to edit password at {user}")
        password = client.recv(1024).decode()
        print(f"Client provided {password} as the new password.")
        status = edit_password(user, password)
        if status == None:
            print("Returned None. Alerting client.")
            client.send("ERROR".encode())
        else:
            print(f"Edited password for {user}. Alerting client.")
            client.send(status.encode())

def main():
    
    while True:
        
        # Establish initial handshake
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        print("Waiting for a connection...")
        client, address = server.accept()
        print(f"Connection from {address}")
        print(f"Sending handshake...")
        client.send("handshake".encode())

        # Handle requests
        message = client.recv(1024).decode()
        if message == "ack":
            print("Recieved ack from client.")
        else:
            print("Ack not recieved. Closing connection...")
            client.close()

        # Await request
        while True:
            request = client.recv(1024).decode()
            if request == "exit":
                print("Client exited.")
                quit() # Temporary exit until we implement threading
            handle_request(request, client)
        

if __name__ == "__main__":
    main()