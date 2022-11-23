import socket
import threading
from function.ultility import *

# Define socket host and port
HOST = '127.0.0.1'
PORT = 8080
allThreadClients = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print("--------------------\n[SERVER]\nListening on port %s ..." % PORT)

def handleClient(connection):
        dataRecv = connection.recv(1024).decode()
        # print(connection)
        request = getRequest(dataRecv)
        if(not request.empty):
            # Send HTTP response
            if(request.method == "GET"):
                getMethod(connection, request)
            if(request.method == "POST"):
                postMethod(connection, request)
            print("--------------------\n[SERVER]\nRequest DONE") 

def Main():
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handleClient, args=(connection,))
        thread.start()
        allThreadClients.append(thread)
        # for thread in allThreadClients:
        #     print(thread)

    for thread in allThreadClients:
        thread.join()
    server.close()

if(__name__ == "__main__"):
    Main()