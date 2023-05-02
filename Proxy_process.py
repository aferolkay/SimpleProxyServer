# Echo server program
import socket
import time
import re

TABLE = []
TABLE.append((0,0))
TABLE.append((1,0))
TABLE.append((2,0))
TABLE.append((3,0))
TABLE.append((4,0))


#decode("OP=ADD;IND=0,1,2;DATA=;")
#Loopback IP address
HOST = '127.0.0.1'
PORT = 6003
#Create a sockets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket successfully created")
# This line avoids bind() exception: OSError: [Errno 48] Address already in use as you configure address reuse
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.bind((HOST, PORT))
print ("Socket is bound to IP:",HOST," PORT:",PORT)
client_socket.listen(1)
print("Listening for connections")
conn, clientAddress = client_socket.accept()
print ('Proxy is connected to the client ', clientAddress)


PORT = 6002
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((HOST,PORT))
print ('Proxy is connected to the server ')

##################################################################################
def decode(command):
    segmentedCommand = re.split(";",command);
    OP = re.split("=",segmentedCommand[0]);
    OP = OP[1];
    INDEX = re.split("=",segmentedCommand[1]);
    INDEX = INDEX[1];
    INDEX = re.split(",",INDEX);
    if INDEX[0]!='':
        for i in range(len(INDEX)):
            INDEX[i] = int(INDEX[i])
    else:
        INDEX = None;
    DATA = re.split("=",segmentedCommand[2]);
    DATA = DATA[1];
    DATA = re.split(",",DATA);
    if DATA[0]!='':
        for i in range(len(DATA)):
            DATA[i] = int(DATA[i])
    #else:
    #    DATA = None; 
    return OP,INDEX,DATA       
        
#####################################################################################

def applyCommand(OP,INDEX,DATA):
    global TABLE

    if OP == "GET":
        for index in INDEX:
            flag=0
            for tuples in TABLE:
                if index == tuples[0]:
                    try :
                        DATA[INDEX.index(index)] = tuples[1]
                    except:
                        DATA.append(0);
                        DATA[INDEX.index(index)] = tuples[1];
                    flag=1
            if flag == 0:
                TABLE.pop(0)
                message = "OP=GET;IND={};DATA=;".format(index)
                server_socket.sendall(bytes(message,'utf-8'))   #contact server for information
                time.sleep(0.5)
                dataReceivedFromServer=server_socket.recv(1024)
                dataReceivedFromServer = dataReceivedFromServer.decode('utf-8')
                opServer,indexServer,dataServer = decode(dataReceivedFromServer);
                TABLE.append((indexServer[0],dataServer[0]))
                try:
                    DATA[INDEX.index(index)] = TABLE[4][1]
                except:
                    DATA.append(TABLE[4][1])
        print(TABLE)           
        returnMessage = "OP=GET;IND={};DATA={};".format(INDEX,DATA)
        return returnMessage
    elif OP == "PUT":
        for index in INDEX:
            flag=0
            message = "OP=PUT;IND={};DATA={};".format(index,DATA[INDEX.index(index)])
            server_socket.sendall(bytes(message,'utf-8'))   
            time.sleep(0.5)
            dataReceivedFromServer=server_socket.recv(1024)
            dataReceivedFromServer = dataReceivedFromServer.decode('utf-8')
            for tuples in TABLE:
                if index == tuples[0]:                   
                    TABLE[TABLE.index(tuples)] = (index,DATA[INDEX.index(index)])            
                    flag=1
            if flag==0:
                opServer,indexServer,dataServer = decode(dataReceivedFromServer)
                TABLE.append((indexServer[0],dataServer[0]))
        print(TABLE) 
        returnMessage = "OP=PUT;IND={};DATA={};".format(INDEX,DATA)        
        return returnMessage                  
        
    elif OP == "CLR":
        message = "OP=CLR;IND=;DATA=;"
        server_socket.sendall(bytes(message,'utf-8'))   
        time.sleep(0.5)
        dataReceivedFromServer=server_socket.recv(1024)
        dataReceivedFromServer = dataReceivedFromServer.decode('utf-8')
        returnMessage = dataReceivedFromServer;
        for tuples in TABLE:
            TABLE[TABLE.index(tuples)] = (tuples[0],0)
        print(TABLE)
        return returnMessage 
    elif OP == "ADD":
        for index in INDEX:
            flag=0
            for tuples in TABLE:
                if index == tuples[0]:
                    try :
                        DATA[INDEX.index(index)] = tuples[1]
                    except:
                        DATA.append(0);
                        DATA[INDEX.index(index)] = tuples[1];
                    flag=1
            if flag == 0:
                TABLE.pop(0)
                message = "OP=GET;IND={};DATA=;".format(index)
                server_socket.sendall(bytes(message,'utf-8'))   #contact server for information
                time.sleep(0.5)
                dataReceivedFromServer=server_socket.recv(1024)
                dataReceivedFromServer = dataReceivedFromServer.decode('utf-8')
                opServer,indexServer,dataServer = decode(dataReceivedFromServer);
                TABLE.append((indexServer[0],dataServer[0]))
                try:
                    DATA[INDEX.index(index)] = TABLE[4][1]
                except:
                    DATA.append(TABLE[4][1])
        print(TABLE)           
        sum=0
        for number in DATA:
            sum += number
        returnMessage = "OP=GET;IND={};DATA={};".format(INDEX,sum)
        return returnMessage
    else:
        print("invalid operation")
        returnMessage = "invalid operation"
    
#####################################################################################

while 1:
    try:
        dataReceivedFromClient = conn.recv(1024)
    except OSError:
        print (clientAddress, 'disconnected')
        client_socket.listen(1)
        conn, clientAddress = client_socket.accept()
        print ('Connected by', clientAddress)
        time.sleep(0.5)

    else:    
        dataReceivedFromClient = dataReceivedFromClient.decode('utf-8')
        #print("Decoded Data is:")
        print("Command Received from Client:{}".format(dataReceivedFromClient))
        OP,INDEX,DATA = decode(dataReceivedFromClient);
        messageToClient = applyCommand(OP,INDEX,DATA)

        #Encode and send the data back to the client
        conn.sendall(bytes(messageToClient,'utf-8'))



