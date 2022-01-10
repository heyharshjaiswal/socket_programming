import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

# instead of bind we are going to connect now...
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)   # To send a message we have to encode it into bytes format.
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))   # padding it to length 64 (HEADER)
    # b' ' -- > is byte representation of the string ' '
    client.send(send_length)
    client.send(message)

send("Hello World!!!")
mes = input("Enter Message: ")
send(mes)
send(DISCONNECT_MESSAGE)
