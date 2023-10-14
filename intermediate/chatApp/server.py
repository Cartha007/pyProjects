# This is a one sided chat app
import socket

s = socket.socket()

host = socket.gethostname()
print(f'Server: {host}')

port = 8080
s.bind((host, port))
print("\nServer done binding to host and port successfully.")
print("Server is waiting for incoming connections")
s.listen(1)
conn, addr = s.accept()
print(f"{addr} Has connected to the server and is now online...")

while True:
    print("Enter your message")
    message = input(str(">"))
    if message != 'q':
        message = message.encode()
        conn.send(message)
        print("Message has been sent...")
        incoming_msg = conn.recv(1024)
        incoming_msg = incoming_msg.decode()
        print(f"Client: {incoming_msg}")
    else:
        break