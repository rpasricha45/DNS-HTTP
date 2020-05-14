#! /usr/bin/env python3
# Echo Client

import sys
import socket
import time
import struct
import random
# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
hostname = sys.argv[3]
# we accept the input as a 4 byte "type of value "
#lengthof data
count = 16
# constants -----------------------------------------------------------
typeOfMessage =1
timeoutTime = 1
messageIdentifier = random.randint(0, 100)
AnswerLength = 0
questionSelection= hostname + ' A IN'
returnCode = 0;
questionLength = len(hostname)
strepQuestionLength = str(questionLength)

messageType= [typeOfMessage,returnCode,messageIdentifier,questionLength,AnswerLength,questionSelection]

myString = ""
for value in messageType:
    myString += str(value) + "!"
# *************************8888***********8
myString = myString.encode()
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(timeoutTime)
memo = "Sending Request " + str(host) + " " + str(port)
# sending message **********************************************************************
try:
    print(memo)
    clientsocket.sendto(myString,(host, port))
    dataEcho, address = clientsocket.recvfrom(count)
    print("Message ID: " + str(messageIdentifier))
    print("Question Length " + str(questionLength) + " bytes")
    print("AnswerLength: 0  bytes")
    print("Question : " + questionSelection)
except socket.timeout as e:
    # if there is a time out try to send 3 times
    print("Request timed out" )
    for i in range(2):

        try:
            print( memo)
            clientsocket.sendto(myString,(host, port))
            dataEcho, address = clientsocket.recvfrom(count)
            print("Ping message number")
        except socket.timeout as e:
            if ( i ==1):
                print("Request timed out.... Exsiting Program")
                break
        print("Request timed out" )
clientsocket.close()
