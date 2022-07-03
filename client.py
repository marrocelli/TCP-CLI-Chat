import socket
import threading
import time


HOST = "localhost"
PORT = 42069
ADDR = (HOST, PORT)
BUFSIZE = 1024
FORMAT = "utf-8"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def receive_messages():
    """
    Receive messages from the server.
    :return: None
    """
    while True:
        try:
            message = client_socket.recv(BUFSIZE).decode(FORMAT)
            print(message)
        except Exception as e:
            print(f"[EXCEPTION] thrown from receive_messages: {e}")
            client_socket.close()
            break


def send_message():
    """
    Sends messages to the server.
    :returns: None
    """
    while True:
        try:
            message = input()
            client_socket.send(message.encode(FORMAT))
        except Exception as e:
            print(f"[EXCEPTION] thrown from send_message: {e}")
            client_socket.close()
            break


# Sending and receiving of messages will be done on their own threads.
receive_thread = threading.Thread(target=receive_messages).start()
send_thread = threading.Thread(target=send_message).start()
