#! /usr/bin/env python3
# Echo Server

import sys
import socket
import time
import struct
import random
def parseTxtFile ():
    # helper funciton that parses a text file and puts it into a map
    # used for dns function
    myMap = {}
    MYFILE = 'dns-master.txt'
    typeClass = "IN"
    with open(MYFILE) as fp:
        myLines = fp.readlines()
        for line in myLines:
            myList = line.split()
            # if the file has comments ignore
            if len(myList) <1:
                continue
            if myList[0] == "#":
                continue
            myKey = myList[0] +  " " + myList[1] +  " " + myList [2]
            record = ""
            for i in range(5):
                record += (myList[i] + " ")
            myMap[myKey] = record
    return myMap
parseTxtFile()

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
messageType =2
# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
myDict = parseTxtFile()

print("The server is ready to receive on port:  " + str(serverPort) + "\n")
# loop forever listening for incoming UDP messages
while True:
    returnCode = 1
    data, address = serverSocket.recvfrom(1024)
    # data = struct.pack('!cclccl', messageType[0],messageType[1],messageType[2],messageType[3],messageType[4],messageType[5])
    print("Responding to ping request")
    answer = 'host-not-exist.student.net A IN'
    myList = data.decode().split("!")
    print(myDict)
    if myList[5] in myDict:

            # answer= myDict[data[5]]
        answer = myDict[myList[5]]
        returnCode = 0



    print("Recieved from " + str(serverIP) + " " +  str(serverPort))
    print("Return Code: " + str(returnCode))
    print("Message Code: " + myList[2])
    print("Question Length :" +  myList[3] + "bytes")
    print("Answer Length" +  str(len(answer)) + " bytes")
    print("Question: "+  myList[5])
    print("Answer: "+ answer)


# prepare to send out new data back to the client **************************
    returnList = []
    returnList.append(messageType)
    returnList.append(returnCode)
    returnList.append(myList[2])
    returnList.append(myList[3])
    returnList.append(len(answer))
    returnList.append(myList[5])
    returnList.append(answer)

    repack = ""
    for element in returnList:
        repack += str(element) + " "
    repack.decode()

    serverSocket.sendto(repack,address)
