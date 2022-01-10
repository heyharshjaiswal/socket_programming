import socket
import threading        
"""
threading is a way of creating multiple threads in a python program
it means if one peace of code(thread) is wating or doing something
then other thread  can run...
So we are going to put all of the message handling stuff in seperate 
threads for each client that connects to a server so that the client 
is not waiting for the other client to respond
"""

# constant values
HEADER = 64
PORT = 5050     # all the ports above 4000 are inactive
# SERVER = "192.168.1.99"   -- can get by "ipconfig" in cmd find "IPv4 Address:" - local IP Address
"""Another way to get the IPv4 address automatically"""
SERVER = socket.gethostbyname(socket.gethostname())
# print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

"""
Steps to Create a Socket:
1) Pick the port        [PORT]
2) Pick the Server      [SERVER]
3) Bind the socket to the address     [ADDR]
"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    """
    handling the specific connections b/w the client and server
    this function will run concurrenlty for each client
    """
    print(f"[NEW CONNECTION] {addr} connected...")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)      # of how many bytes we want to receive a message
        if msg_length:      # if not this line then : ValueError: invalid literal for int() with base 10: '' 
            # because there should be the some length to a message...
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            print(f"[{addr}] {msg}")
    
    conn.close()


def start():
    """to add new connections and distributes"""
    server.listen()     # listening a new connections
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:         # continue listening infinitely until server crashes
        conn, addr = server.accept()        # accepts a new connection and saves the port and ip address
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}") # tells us the number of active threads
            # and each thread repesents an active connection and since there is always 1 thread running i.e. 
            # start() thread so '- 1'


print("[STARTING] server in starting")
start()

