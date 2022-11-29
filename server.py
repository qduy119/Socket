import socket
import threading
import sys
from function.ultility import *

# Define socket host and port
HOST = '127.0.0.1'
PORT = 8080

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("Error creaing socket: %s"%(err))
    sys.exit(1)

try:
    server.bind((HOST, PORT))
except socket.error as err:
    print("Error binding: %s"%(err))
    sys.exit(1)

server.listen(5)
print("--------------------\n[SERVER]\nListening on port %s ..." % PORT)

def handleClient(connection, address):
    print("Connection %d: (%s, %s)"%(threading.active_count(), address[0], address[1]))
    while True:
        try:
            reqRecv = connection.recv(2048).decode("utf-8")
        except socket.error as err:
            print("Error receiving request: %s"%(err))
            sys.exit(1)

        request = getRequest(reqRecv)

        if(not request.empty):
            # GET Method
            if(request.method == "GET"):
                try:
                    connection.sendall(Response(request.path))
                except socket.error as err:
                    print("Error sending response: %s"%(err))
                    sys.exit(1)

            # POST Method
            if(request.method == "POST"):
                try:
                    if(request.content == "uname=admin&psw=123456&remember=on" or request.content == "uname=admin&psw=123456"):
                        connection.sendall(Response(request.path))
                    else:
                        connection.sendall(Response("/401.html"))
                except socket.error as err:
                    print("Error sending response: %s"%(err))
                    sys.exit(1)
            print("--------------------\n[SERVER]\nRequest %s with path %s DONE\n"%(request.method,request.path))
    connection.close()

if(__name__ == "__main__"):
    while True:
        try:
            connection, address = server.accept()
        except socket.error as err:
            print("Error accepting connection: %s"%(err))
            sys.exit(1)

        thread = threading.Thread(target=handleClient, args=(connection, address))
        thread.start()        

    server.close()
