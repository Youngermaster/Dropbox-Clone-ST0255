import os
import socket
import threading
import argparse

# * Config constatns
HEADER = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
ROOT_DIR = os.path.dirname(os.path.abspath("client.py")) + "/buckets"

# ! Initialized socket server globally
# * AF_INET correspond to IPV4
# * SOCK_STREAM correspond to TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


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

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

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
