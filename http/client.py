import os
import socket
import itertools
import sys


def getCacheList(filename):
    with open(filename, 'r') as file:
    # read a list of lines into data
        data = file.readlines()
        return data
def inCache ( myList,object):
    # returns -1 if not presetn and the "id"

    if len(myList) == 0:
        return -1
    for i  in range(len(myList)):
        if myList[i].split()[0] == 'OBJ':
            if myList[i].split()[1] == object:
                return i
    return -1

def findEnd ( myList, start,object):
    # if returns 0 , then the cache is empty of valid
    # returns the start of where you should add

    for i in range(start , len(myList) ):
        line = myList[i]
        segments = line.split()
        if segments[0] == 'OBJ':
            return i

        return len(myList)


def get (host , port,type,object):

    data = """GET /""" + object + """ HTTP/1.1
    host: """ + host +"""

    """


    if len(type) >0:
        condStatement = "If-Modified-Since: " + type + "\r\n"
        data = data + '\r\n' + condStatement
    else:
        data += "\r\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, int(port)))

    sock.sendall(data.encode())
    data = b''
    while True:
        buf = sock.recv(1024)
        if not buf:
            break
        data += buf
    sock.close()
    print(data.decode())
    return data.decode()

def putToCache(fileName,data,object):
    # function that put the server resonse in the cache
    id = "OBJ "+object + '\r\n'
    data = id +data

    with open(fileName, "a") as myfile:
        myfile.write(data)

myArg = str(sys.argv [1])
HOST = myArg[0:myArg.index(":")]
PORT = myArg[myArg.index(":")+1:myArg.index("/")]
OBJECT = myArg[myArg.index("/") +1:]

try:
    f = open("cache.txt")
    # Do something with the

except IOError:
    # todo create cache .txt
    f= open("cache.txt","w+")
# this is obsloutlte and defeates the purposes - of the program

myList = getCacheList("cache.txt")

index =  inCache(myList,OBJECT)


# not in my cache
if index == -1:

    serverResponse =get(HOST,PORT,"",OBJECT)
    header = serverResponse.split()[1]
    if header != '404':
        putToCache("cache.txt",serverResponse,OBJECT)
else:

    lastModfied = myList[4][myList[4].index(':')+2:]
    result = get(HOST,PORT,lastModfied,OBJECT)
    resHeader = result.split()[1]
    if resHeader == '304':
        # file not Modified

        sys.exit(1)
    elif resHeader == '404':
        print(result)
    else:

        newCache = []
        firstElement = "OBJ " +OBJECT
        newCache.append(firstElement)
        endInterval = findEnd(myList , index+1, OBJECT)
        for i in range(len(myList)):
            if ( i < index or i >=endInterval):
                myList.append(newCache)
        # write the new fileData
        with open("cache.txt", "w") as myfile:
            for lines in newCache:
                myfile.write(lines + "\n")
            myfile.write(result)


f.close()
