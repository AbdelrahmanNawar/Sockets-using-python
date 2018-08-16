import socket
import sys


def main(theHost="localhost", thePort=8888):
    print("#LocalMsg#\n\t", theHost, thePort)
    myClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        myClientSocket.connect((theHost, thePort))
    except socket.error as e:
        sys.exit('Connection failed. \nERROR Code : ' + str(e.errno) + '\nMessage : ' + str(e.strerror))

    ''' after this point the client should be connected
        the server will send a confirmation msg'''
    # the client request should follow this format: GET/POST file-name host-name (port-number)
    result = myClientSocket.recv(1024).decode("utf-8")
    print("#ServerMsg#\tNOTE :\n" + result)

    while True:
        request = input(">> ")
        myClientSocket.send(request.encode("utf-8"))
        if request == "q":
            '''or request == "quit" # this one makes an error!'''
            print("#LocalMsg#\n\tConnection closed!")
            break
        response = myClientSocket.recv(1024).decode("utf-8")
        print("#ServerMsg#\n" + response)
        if "200 OK" in response:
            handlingTheResult(myClientSocket, request)


def handlingTheResult(myClientSocket, request):
    request = request.split()
    if "GET" == request[0]:
        with open(request[1], "w") as theFile:
            while True:
                dataChunk = myClientSocket.recv(1024).decode("utf-8")
                if not dataChunk:
                    break
                theFile.write(dataChunk)
    elif "POST" == request[0]:
        with open(request[1], "r") as theFile:
            while True:
                dataChunk = theFile.read(1024)
                if not dataChunk:
                    break
                myClientSocket.send(dataChunk.encode("utf-8"))
    print("SHIT!")

    while True:
        result = myClientSocket.recv(1024).decode("utf-8")
        if not result:
            break


if __name__ == "__main__":
    try:
        server_ip = sys.argv[1]
        port_number = int(sys.argv[2])
        if port_number < 0:
            sys.exit("(((Wrong Port Number ~ Server Exit !)))")
    except ValueError:
        sys.exit("(((The Args/Prams must be NUMBERS !)))")
    except IndexError:
        server_ip = "localhost"
        port_number = 8888
    main(server_ip, port_number)
