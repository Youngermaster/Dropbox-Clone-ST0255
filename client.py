import socket

# * Config constatns
HEADER = 4096 # send 4096 bytes each time step
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# ! If you run the code from different machines on the same network
# ! uncomment the line below and comment the other one called SERVER too
# SERVER = "127.0.1.1"
# ! If the code runs on the same machine let this automatic IP
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

# * AF_INET correspond to IPV4
# * SOCK_STREAM correspond to TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


if __name__ == "__main__":
    print(f"[LISTENING] Server is listening on {SERVER}")
    print(f"[SUCCESS] Succesfully connected to {SERVER}")
    connected = True
    while connected:
        print("Type a command, if you are not sure use !HELP command to get more info:")
        msg = input()
        if msg == DISCONNECT_MESSAGE:
            connected = False
        else:
            send(msg)