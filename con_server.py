import socket
import sys
from _thread import *

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        try:
        #Receiving from client
            data = conn.recv(1024)
            if data:
            	print(data)
        except socket.error:
        	conn.close()
    
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8889 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except:
	sys.exit()
 
#Start listening on socket
s.listen(10)
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()