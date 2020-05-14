import os
import socket
import sys
import datetime , time


def getFileData (fileName):
    # helper method that gets the data and returns it
    # if not there - returns empty string use that for parsing
    rtVal = ""
    try:
        f = open(fileName)
        myLines = f.readlines()
        for line in myLines:
            rtVal += line
        return rtVal

    except IOError:
        print("Todo 404 file not found - please implement")
        return rtVal
HOST = sys.argv[1]
PORT = sys.argv[2]

# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 65433
print("starting server")
# source : https://wiki.python.org/moin/TcpCommunication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((serverIP, serverPort))
# cmd arguments are ip and port
s.bind((HOST, int(PORT)))
s.listen()
conn, addr = s.accept()
with conn:
    # todo put the current time


    print('Connected by', addr)
    data = conn.recv(1024)
    data = data.decode()

    # todo need to parse
    print("data")
    print(data)
    fileName = data.split()[1][1:]
    print("filename")
    print(fileName)

    # parse if the file is valid = you need to this
    t= epoch_time = int(time.time())
    t= time.gmtime(t)
    currentTime ="Date "+ time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", t)
    try:
        f=open(fileName)
    except IOError:
        result = "HTTP/1.1 404 Not Found \r\n"+currentTime+"\r\n"
        conn.sendall(result.encode())
        sys.exit(0)


    # todo implement the last modtime
    statbuf = os.stat(fileName)
    t = time.gmtime(statbuf.st_mtime)
    modTime = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n", t)
    lastMod = "Last-Modified: " +modTime
    # todo implement content length
    contLen = "Content-Length: " + str(statbuf.st_size )
    result = "HTTP/1.1 200 OK \r\n" + currentTime + "\r\n" + lastMod +  contLen + "\r\n Content-Type: text/html; charset=UTF-8\r\n\r\n"

    fileN = data.split()[1]
    print(fileN + " this is the file")
    # todo parse the data to get the name of the objecy - you need to change
    # Determine the if conditioanal window
    fileData = getFileData(fileName)

    print("printing out client : data sent ")
    print(data)
    print(data.split())
    print(len(data.split()))
    print("testing if lastmod ")


    if len(fileData) < 1:
        # there is no file in record
        result = "HTTP/1.1 404 Not Found \r\n"+currentTime+"\r\n\r\n"
        conn.sendall(result.encode())



    elif ( len(data.split()) >5 and data.split()[5] == "If-Modified-Since:"):
        print("entering in coditional request")
        # assuming that the date length is constant
        # extract it and compare
        print(data)
        testTime = data.split()[6:12]
        print("testTimeds")
        print(testTime)
        clientTime = ""
        for time in testTime:
            clientTime+=time+ " "
        print(clientTime + " clientTime")
        print(modTime + "modTime")

        # todo change the last modified

        if modTime.split() == clientTime.split():
            # send the coditional get
            print("they are the same !")
            result = "HTTP/1.1 304 Not Modified\r\n"+currentTime+"\r\n\r\n"
            conn.sendall(result.encode())

        else:

            print('they modtime and client are not the same ')
            print(modTime.split())
            print(clientTime.split())
            print(len(modTime) - len(clientTime) )


            result += fileData
            conn.sendall(result.encode())

    else:
        result += fileData
        print("sending")
        conn.sendall(result.encode())
