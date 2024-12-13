import socket
import json

host = "127.0.0.1"
port = 56789
list_file = "list.json"

'''
Function: write_list
Purpose: Writes the password list into persistent memory as a json file
Parameters: passwords
'''
def write_list(passwords):
    print("Saving list...")
    with open(list_file, "w") as outfile:
        json.dump(passwords, outfile, separators=(",\n", ": "))
    print("List saved")

'''
Function: read_list
Purpose: Reads the passwords in persistent memory and updates the list
Parameters: None
'''
def read_list():
    print("Reading list...")
    with open(list_file, "r") as outfile:
        passwords = json.load(outfile)
    print("List read")
    return passwords

# Load passwords from file
passwords = read_list()

'''
Function: new_password
Purpose: Adds a new entry to the password list and writes it into memory
Parameters: user, password, passwords
'''
def new_password(user, password, passwords):
    print(f"Writing entry for {user}:{password} to disk...")
    passwords[user] = password
    write_list(passwords)

'''
Function: retrieve_password
Purpose: After reading an updated list, retrieve a password under the given username
Parameters: user
'''
def retrieve_password(user):
    print(f"Retrieving entry for {user}...")
    passwords = read_list()
    return passwords[user]

'''
Function: retrieve_all
Purpose: Retrieve the full password list
Parameters: None
'''
def retrieve_all():
    print(f"Retrieving whole list")
    passwords = read_list()
    print(passwords)
    return json.dumps(passwords)

'''
Function: delete_password
Purpose: Delete the password under a given username
Parameters: user
'''
def delete_password(user):
    print(f"Deleting entry for {user}...")
    passwords = read_list()
    if passwords.pop(user, None) == None:
        print(f"No entry for {user}. Returning None.")
        return None
    else:
        write_list(passwords)
        return "SUCCESS"

'''
Function: edit_password
Purpose: Change the password under a given user with a new given password
Parameters: user, password
'''
def edit_password(user, password):
    print(f"Updating entry for {user} with new password {password}...")
    passwords = read_list()
    if user in passwords:
        print(f"Found entry for {user}...")
        passwords[user] = password
        print(f"Updated password.")
        write_list(passwords)
        return "SUCCESS"
    else:
        return None

'''
Function: handle_request
Purpose: Largest, primary function on the server.
This function continuously loops and handles requests sent from the client.
Parameters: user
'''
def handle_request(request, client):

    if request == "new":
        passwords = read_list()
        print("Making a new password!")
        password = client.recv(1024).decode()
        print(f"Client sent {password}")
        user = client.recv(1024).decode()
        print(f"Client sent {user}")
        new_password(user, password, passwords)

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
        passwords = read_list()
        client.send(json.dumps(passwords).encode())

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
        #write_list(passwords)

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
        print("Starting main loop")
        print("===================")
        while True:
            request = client.recv(1024).decode()
            if request == "exit":
                print("Client exited.")
                break
            handle_request(request, client)
        

if __name__ == "__main__":
    main()