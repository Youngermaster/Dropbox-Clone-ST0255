import os
import socket
import threading
import argparse

# * Config constatns
HEADER = 4096 # send 4096 bytes each time step
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
ROOT_DIR = os.path.dirname(os.path.abspath("client.py")) + "/buckets"

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

            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg == HELP:
                help(conn)
            elif msg == CREATE_BUCKET:
                create_bucket("name")
            elif msg == CREATE_BUCKET:
                delete_bucket("name")
            elif msg == LIST_BUCKETS:
                list_buckets()
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
    conn.send("Help".encode(FORMAT))


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


def list_buckets():
    if len(buckets) == 0:
        print("There isn't any buckets")
        print(
            f"If you want to create one bucket use the following command {CREATE_BUCKET}")
    else:
        pass
    print(f"List of buckets:\n{buckets}")


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
    start(buckets_path)
