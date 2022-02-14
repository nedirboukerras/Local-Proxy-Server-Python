from socket import *

def existinFile(e,f):
    for i in f:
        if e==i:
            return(1)
    return(0)

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5678

# Proxy Censeur infos
censeurName='127.0.0.1'
censeurPort=1235

# Loggeur Proxy infos
loggeurName='127.0.0.1'
loggeurPort=5679

# Server infos
serverName='127.0.0.1'
serverPort=1234

# Create socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:    
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()
    GET=request.split('\n')[0].split()[1]
    if GET == '/':
        GET = '/index.html'
    
    #client for proxyCenseur part
    clientSocket= socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((censeurName,censeurPort))
    message=GET
    clientSocket.send(message.encode())
    serverMessage=clientSocket.recv(1024).decode('utf-8')   
    response =  serverMessage
    clientSocket.close()

    #client for proxyLoggeur part
    clientSocket= socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((loggeurName,loggeurPort))
    message=request
    
    if(response=='OK'):
        if(GET.find(".html")!=-1):
            openCache=open('cache.txt')
            readCache=openCache.readlines()
        
            if(existinFile(GET+'\n',readCache)==1):
          
                # Get the content of the file
                try:
                    print("Proxy did it")
                    fin = open('htdocs' + GET)
                    content = fin.read()
                    fin.close()
                    
                    # Send HTTP response
                    response = 'HTTP/1.0 200 OK\n\n' + content
                    client_connection.sendall(response.encode())
                    client_connection.close()
                    message=message+' '+response
                    clientSocket.send(message.encode())
                    clientSocket.close()
                except FileNotFoundError:
                    response = 'HTTP/1.0 200 OK\n\n'+'<html><body><h1>404 NOT FOUND</h1>\n\n'+GET+' : File Not Found</body></html>'
                    client_connection.sendall(response.encode())
                    client_connection.close()
                    message=message+' '+response
                    clientSocket.send(message.encode())
                    clientSocket.close()
            else:
           
                clientSocketwithServer= socket(AF_INET,SOCK_STREAM)
                clientSocketwithServer.connect((serverName,serverPort))
                message=GET
                clientSocketwithServer.send(message.encode())
                serverMessage=clientSocketwithServer.recv(4096).decode('utf-8')
            
                response =  serverMessage
                client_connection.sendall(response.encode())
                openCache=open('cache.txt','a+')
                openCache.writelines(GET+'\n')
                openCache.close()
                
                clientSocketwithServer.close()
                client_connection.close()
                message=request+' '+response
                clientSocket.send(message.encode())
                clientSocket.close()

    else:  
        client_connection.sendall(response.encode())     
        client_connection.close() 
        message=message+' '+response
        clientSocket.send(message.encode())
        clientSocket.close()