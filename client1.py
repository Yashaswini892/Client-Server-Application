import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# Initialize colors
init()

# Set available colors
color_choices = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
                 Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
                 Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
                 Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
                 ]

# Choose a random color for the client
client_color = random.choice(color_choices)

# Server configuration
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5430
separator_token = "<SEP>"

# Initialize TCP socket
client_socket = socket.socket()
print(f"Connecting to {SERVER_IP}:{SERVER_PORT}...")
client_socket.connect((SERVER_IP, SERVER_PORT))
print("CONNECTED TO THE SERVER")

# Prompt the client for a name
client_name = input("Enter your client name: ")


def receive_and_display_messages():
    while True:
        received_message = client_socket.recv(1024).decode()
        print("\n" + received_message)


# Create a thread for listening to messages and printing them
message_thread = Thread(target=receive_and_display_messages)
message_thread.daemon = True
message_thread.start()

while True:
    # Input message to send to the server
    message_to_send = input()
    # Check for exit command
    if message_to_send.lower() == 'q':
        break
    # Include the name and color of the sender
    formatted_message = f"{client_color}{client_name}{separator_token}{message_to_send}{Fore.RESET}"
    print("formatted msg ", formatted_message)
    # Send the message
    client_socket.send(formatted_message.encode())

# Close the socket
client_socket.close()
