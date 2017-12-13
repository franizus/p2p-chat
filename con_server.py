import socket
import sys
import threading


def clientthread(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                print(data)
        except socket.error:
            client_socket.close()


HOST = ''
PORT = 8889

SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    SERVER_SOCKET.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

SERVER_SOCKET.listen(10)
THREADS = []

while 1:
    connection, address = s.accept()
    THREADS.append(threading.Thread(target=clientthread, args=(connection,)).start())

SERVER_SOCKET.close()
