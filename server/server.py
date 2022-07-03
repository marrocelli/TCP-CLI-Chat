import threading
import socket
import time
from user import User

# GLOBAL CONSTANTS
HOST = "localhost"
PORT = 42069
ADDR = (HOST, PORT)
BUFSIZE = 1024
MAX_CONNECTIONS = 5
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "quit"

# GLOBAL VARIABLES
users = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def broadcast(message):
    """
    Sends new messages to all clients.
    :param ...:
    """
    for user in users:
        client = user.client
        try:
            client.send(message)
        except Exception as e:
            print(f"[EXCEPTION] thrown from broadcast: {e}")


def handle_client(user):
    """
    Handles interactions with single client connection and server. 
    :params user: User object
    :return: None
    """

    client = user.client

    # Send message to client to enter their name.
    client.send("Enter your name".encode(FORMAT))
    # first message received is always the person's name
    name = client.recv(BUFSIZE).decode(FORMAT)
    user.set_name(name)

    # Broadcast that user has joined the chat once they have entered their name.
    broadcast(f"{user.name} has joined the chat".encode(FORMAT))
    

    while True:
        # This is the main loop for communication and will run until the user closes their command prompt window,
        # enters the DISCONNECT_MESSAGE, or another error occurs.
        try:
            message = client.recv(BUFSIZE).decode(FORMAT)

            if message != DISCONNECT_MESSAGE: # If message is not DISCONNECT_MESSAGE, send message to all active clients.
                message = f"{user.name}: {message}".encode(FORMAT)
                broadcast(message)
            else: # Else, disconnect client and notify other clients.
                client.send("You have been disconnected.".encode(FORMAT))
                users.remove(user)
                client.close()
                broadcast(f"{user.name} has left the chat.".encode(FORMAT))
                break
                
        except:
            users.remove(user)
            client.close()
            broadcast(f"{user.name} has left the chat.".encode(FORMAT))
            break


def accept_incoming_connections():
    """
    Wait for new connections from clients, start new thread to handle interactions once connected.
    :return: None
    """
    while True:
        try:
            # This line blocks while waiting for a new connection to the server.
            client, address = server.accept()
            new_user = User(client, address)
            users.append(new_user)
            print(f"[NEW CONNECTION] {address} connected to the server at {time.strftime('%I:%M%p')}")
            
            # Let the client know that they have succesfully connected to the server.
            client.send("Connected to the server.".encode(FORMAT))

            # Start new thread to hande communication with client.
            thread = threading.Thread(target=handle_client, args=(new_user,))
            thread.start()
        except Exception as e:
            print(f"[EXCEPTION] thrown from accept_incoming_connections: {e}")
            break
    
    print("SERVER CRASHED")



if __name__ == "__main__":
    # Open server to listen for new connections.
    server.listen(MAX_CONNECTIONS)
    print(f"[LISTENING] Server is listening on {HOST}")

    # Create new thread for accepting server connections.
    ACCEPT_THREAD = threading.Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()

    # Call .join() method so that server script waits for ACCEPT_THREAD to complete before continuing to next line
    # which closes the chat server.
    ACCEPT_THREAD.join()
    server.close()
