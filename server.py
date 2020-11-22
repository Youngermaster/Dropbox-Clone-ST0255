import os
import socket
import threading
import argparse

# * Config constatns
HEADER = 4096  # send 4096 bytes each time step
PORT = 4040
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
ROOT_DIR = os.path.dirname(os.path.abspath("server.py"))
BUCKETS_FOLDER = "BUCKETS"

# * Commands
DISCONNECT_MESSAGE = "!DISCONNECT"
HELP = "!HELP"
# * Bucket commands
CREATE_BUCKET = "!CREATEB"
DELETE_BUCKET = "!DELETEB"
LIST_BUCKETS = "!LISTB"
# * File Commands
UPLOAD_FILE = "!UPLOADF"
DELETE_FILE = "!DELETEF"
LIST_FILES = "!LISTF"
DOWNLOAD_FILE = "!DOWNLOADF"

# ! Initialized socket server globally
# * AF_INET correspond to IPV4
# * SOCK_STREAM correspond to TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

buckets = []


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == HELP:
                help(conn)
            elif CREATE_BUCKET in msg:
                create_bucket("name")
            elif DELETE_BUCKET in msg:
                delete_bucket("name")
            elif msg == LIST_BUCKETS:
                list_buckets(conn)
            elif msg == UPLOAD_FILE:
                upload_file("name")
            elif msg == DELETE_FILE:
                delete_file("name")
            elif msg == LIST_FILES:
                list_files("name")
            elif msg == DOWNLOAD_FILE:
                download_file("name")

            print(f"[{addr}] {msg}")
            conn.send("[SUCCESS] Message received".encode(FORMAT))

    conn.close()

# * Starts the socket server
# @param buckets_path This is the "directory" where will be stored
#  all the buckets


def start(buckets_path):
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    print(f"The Buckets will be storage in: {buckets_path}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def help(conn):
    help_message = "Help message"
    conn.send(help_message.encode(FORMAT))


def create_bucket(bucket):
    if bucket in buckets:
        print("Bucket name already exist")
    else:
        print("Bucket created succesfully")


def delete_bucket(bucket):
    if bucket in buckets:
        print("Bucket name already exist")
    else:
        print("Bucket created succesfully")


def list_buckets(conn):
    list_of_buckets_message = "j"
    if len(buckets) == 0:
        list_of_buckets_message = "There isn't any buckets\n"
        list_of_buckets_message += f"If you want to create one bucket use the following command {CREATE_BUCKET}"
    else:
        list_of_buckets_message = f"List of buckets:\n{os.listdir()}"

    conn.send(list_of_buckets_message.encode(FORMAT))


def upload_file(bucket_owner):
    pass


def delete_file(bucket_owner):
    pass


def list_files(bucket_owner):
    pass


def download_file(bucket_owner):
    pass


if __name__ == "__main__":
    print("[STARTING] server is starting...")
    # * We create the CLI arguments
    parser = argparse.ArgumentParser(description="Dropbox Clone ST0255")

    # * We create the "directory" flag to store all the buckets
    parser.add_argument(
        "-d", "--directory", help="Folder to store all the buckets, the default directory is the project directory",
        default=ROOT_DIR)

    args = parser.parse_args()
    buckets_path = args.directory

    # Path
    dir_path = os.path.join(buckets_path, BUCKETS_FOLDER)

    # Create the directory
    # 'buckets'
    try:
        os.rmdir(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))
    try:
        os.makedirs(dir_path, exist_ok=True)
        print("Bucket directory '%s' created successfully" % BUCKETS_FOLDER)
    except OSError as error:
        print("Bucket directory '%s' can not be created" % BUCKETS_FOLDER)
    start(buckets_path)
