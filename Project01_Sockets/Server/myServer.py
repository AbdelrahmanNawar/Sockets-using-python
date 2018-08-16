import socket
import sys
import threading  # thread per request
import multiprocessing  # process per client
from os import path


# import regex  # for parsing and validation

def main(numOfClients = 5, theHost="localhost", thePort=80):
    print("#LocalMsg#\n\t", numOfClients, theHost, thePort)
    myServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        myServerSocket.bind((theHost, thePort))
    except socket.error as e:
        sys.exit('Binding failed. \nERROR Code : ' + str(e.errno) + '\nMessage : ' + str(e.strerror))
    myServerSocket.listen(numOfClients)
    print("#LocalMsg#\n\tServer started and waiting for a connection!\n")
    while True:
        connectionSocket, address = myServerSocket.accept()
        # multiprocessing code
        myProcess = multiprocessing.Process(target=processJob, args=(connectionSocket, address))
        myProcess.start()
    # TAG:Debugging? how to reach this (get out of the loop)
    myServerSocket.close()

def processJob(connectionSocket, address):
    print("#LocalMsg#\n\tconnected to : " + address[0] + ":" + str(address[1]))
    connectionSocket.send("Connected to the Server!\n"
                          "HTTP requests should be on this format:\n"
                          "GET/POST file-name host-name (port-number)".encode("utf-8"))    
    while True:
        print ("2 a7teen") 
        data = connectionSocket.recv(1024).decode("utf-8")
        print("> incoming data \n" + data)
        if not data or data == "q":
            '''or request == "quit" # no working!'''
            break
        myThread = threading.Thread(target=threadJob, args=(connectionSocket, data))
        myThread.setDaemon(True)  # to end the thread if the main thread ends
        myThread.start()
    connectionSocket.close()
    print("Connection closed!")


def threadJob(connectionSocket, request):
    data = request.split()
    if data[0] == "POST":
        sendHTTPStatusMsg(connectionSocket, 200)
        with open(data[1], 'w') as theFile:
            while True:
                chunkData = connectionSocket.recv(1024).decode("utf-8")
                if not chunkData:
                    break
                theFile.write(chunkData)
    elif data[0] == "GET":
        if path.exists(data[1]):
            sendHTTPStatusMsg(connectionSocket, 200)
            with open(data[1], 'r') as theFile:
                while True:
                    line = theFile.read(1024)
                    connectionSocket.sendall(line.encode("utf-8"))
                    if line == "":
                        break
        else:
            sendHTTPStatusMsg(connectionSocket, 404)
    else:
        connectionSocket.send(("Invalid text: " + request).encode("utf-8"))


def sendHTTPStatusMsg(connection, statusCodes):
    # TAG:Debugging? share memory between processes OR Leave it as a function
    HTTPStatusCodes = {
        200: "200 OK",
        404: "404 Not Found",
        400: "400 Bad Request"
    }
    connection.send(("HTTP/1.0 " + HTTPStatusCodes[statusCodes] + "\r\n").encode("utf-8"))


if __name__ == "__main__":
    try:
        thePort = int(sys.argv[1])
        numOfClients = int(sys.argv[2])
        if thePort < 0 or numOfClients < 1:
            sys.exit("(((Wrong Port Number ~ Invalid amount of clients ~ Server Exit !)))")
    except ValueError:
        sys.exit("(((The Args/Prams must be NUMBERS !)))")
    except IndexError:
        thePort = 8888  # TAG:Debugging delete
        numOfClients = 3
        theHost = "localhost"
        pass
    main(numOfClients, theHost, thePort)
