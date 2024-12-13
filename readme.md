<!-- ABOUT THE PROJECT -->

## Password Manager

CLI password manager built in Python designed to be run on a home server.

### Server.py

Be sure to update `server.py` so that `host` and `port` are your host machine IP and desired port address. By default it uses the localhost `127.0.0.1` but should be the host machine's address.

### Client.py

Client is self-explanatory. It should be placed on your client machine. Be sure `host` and `port` match what is set on your server.

The client is capable of running the following commands:

```
n - New Password
r - Retrieve Password
d - Delete Password
e - Edit Password
l - Retrieve List
q - Quit
```

### List.json

This is the persistent password list. All entries are encrypted on the client-side before being sent to the server. The server and host machine is unable to read any passwords directly.

### Key

This file is extremely important. If it gets deleted the passwords are not recoverable and will need to be deleted. You should use `python generate_key.py` to create a new key before use. Passwords will also be unreadable if the key is changed.

### Generate_key.py

Generates the key for encryption. If using multiple clients the same key should be copied to each client directory.

### Getting Started

1. Getting started with this project is simple. The directory structure should look as follows:

password_manager/
├─ client.py
├─ generate_key.py
├─ key
├─ list.json
├─ server.py
├─ README.md

2. Assuming this is your first time using this program you will need to generate a new key.

```
PS D:\Projects\password_manager> python .\generate_key.py
Only run this if you would like to regenerate the key. Doing so will render previous passwords unreadable.
Are you sure you want to continue? y/n
y
Wrote key to file
```

3. Next you should delete the example passwords in `list.json`. The resulting file should look as follows:

```
{}
```

4. Copy the necessary files to your server. The directory should look as follows:

server/
├─ list.json
├─ server.py

5. Launch

```
python .\server.py
```

6. Copy the necessary files to your client. The directory should look as follows:

client/
├─ client.py
├─ generate_key.py
├─ key

7. Launch

```
python .\client.py
```
