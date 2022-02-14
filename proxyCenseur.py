from socket import *

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1235

# Server infos
serverName='127.0.0.1'
serverPort=1234


#Cache infos
cacheName='127.0.0.1'
cachePort=5678

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
    GET = client_connection.recv(1024).decode()
   
    interdit=open('interdit.txt')
    interditRead=interdit.readlines()
   
    if(GET.find(".html")!=-1):
        
        if(GET+'\n' in interditRead):
            response = 'HTTP/1.0 200 OK\n\n'+'<html><body><h1>URI INTERDIT</h1>\n\n'+GET+' : SITE WEB INTERDIT</body></html>'
            client_connection.sendall(response.encode())
            client_connection.close()

        else:   
            response = 'OK'
            client_connection.sendall(response.encode())
            client_connection.close()
    else : client_connection.close()    