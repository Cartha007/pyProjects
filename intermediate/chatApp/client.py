import socket

s = socket.socket()
host = input(str("Please enter the hostname of the server: "))
port = 8080
s.connect((host,port))
print("Connected to chat server.")

while True:
    incoming_msg = s.recv(1024)
    incoming_msg = incoming_msg.decode()
    print(f"Server: {incoming_msg}")
    print("Enter your message")
    message = input(str(">"))
    if message != 'q':
        message = message.encode()
        s.send(message)
        print("Message has been sent...")
    else:
        break