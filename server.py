import socket
from threading import Thread

# Configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5430
TOKEN_SEPARATOR = "<SEP>"

# Maintain a set of connected client sockets
active_clients = set()

# Create a TCP socket
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(10)
print(f"Server started at {SERVER_IP}:{SERVER_PORT}")


def handle_client_connection(client_socket):
    """
    Function to handle messages from a connected client and broadcast them to others.
    """
    while True:
        try:
            # Receive a message from the client
            message = client_socket.recv(1024).decode()
            print("msg",message)
        except Exception as error:
            # Client disconnected, remove from the set
            print(f"[!] Error: {error}")
            active_clients.remove(client_socket)
            break
        else:
            # Replace the separator token with ": " for printing
            formatted_message = message.replace(TOKEN_SEPARATOR, ": ")

        # Broadcast the formatted message to all connected clients
        for other_client in active_clients:
            if other_client != client_socket:
                other_client.send(formatted_message.encode())


while True:
    # Accept a new client connection
    client_socket, client_address = server_socket.accept()
    print(f"[+] {client_address} connected.")
    
    # Add the new client to the set of connected clients
    active_clients.add(client_socket)
    
    # Start a new thread to handle the client's messages
    message_handler_thread = Thread(target=handle_client_connection, args=(client_socket,))
    message_handler_thread.daemon = True
    message_handler_thread.start()
