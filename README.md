General Information
In this assignment I was able to successfully implement 
• a server in MATLAB
• a proxy server in python and 
• a client in python.
The system supports 4 commands which are, PUT, ADD, GET, CLR. Communication between 
each system is in the form of “OP=XXX;IND=IND0,IND1,…,INDn;DATA=DATA0,DATA1,…,DATAn”. The 
system supports up to 5 indexes and data in each command.
Client – Proxy - Server Connection
The server has the IP '127.0.0.1' and opens a socket in port 6002 and the proxy connects to it 
using the IP and port information. The proxy has 2 sockets, one for connecting to the main server. The 
other socket has the same IP of '127.0.0.1' and port number 6003 for serving functionality. Finally the 
client has one client and will connect to port number 6003 of the proxy.
To achieve a successful running communication network, run the server first, then the proxy 
server. Finally, the client should be run. The program will have information printed on the terminals
about connection status.
The proxy server contains 5 slots for data whereas the main server will have 10. The proxy 
stores these last requested data slots for future use if applicable. If new data is required by the client, 
then the data is fetched from the main server and overwrites the oldest data slot.
If the proxy server does not have enough information to serve the client, it will act as a client 
itself and request the actual command to the main server and return the data received from it to 
serve the actual client.
The client terminal waits for user input and then sends the message to the proxy server and 
waits for a response to show. The socket makes it possible to pass information between different 
programming environments and different processes. 
Commands
• PUT Command (OP=PUT;IND=IND0,IND1,…,INDn;DATA=DATA0,DATA1,…,DATAn)
It saves the data written in the DATA to its respective places, specified in INDEX. Supports up 
to 5 index-data points. Proxy server and the main server will print database to the console.
• ADD Command (OP=ADD;IND=IND0,IND1,…,INDn;X,X)
It takes the index specified in IND part and captures the responding data values from the 
table and sums these values. It doesn’t matter what the client wrote in DATA location.
Supports up to 5 index-data points. The data is returned to the client in the receiving 
message’s DATA part.
• GET Command (OP=GET;IND=IND0,IND1,…,INDn;DATA=X,X,X)
It takes the indexes specified in IND part and captures the responding data values from the 
table and places these values in the DATA part of the message returned to the client. It 
doesn’t matter what the client wrote in DATA location, it is overwritten in the returning 
message. Supports up to 5 index-data points. The data is returned to the client in the 
receiving message’s DATA part.
• CLR Command (OP=CLR;IND=X,X,…,X;DATA=X,X,...,X)
Clears all the data on the table of the server and initializes all 10 data values to 0. Server will 
print database to the console.
