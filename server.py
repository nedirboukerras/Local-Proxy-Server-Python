from socket import *

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1234

# Create socket
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True: 
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    GET = client_connection.recv(999999).decode()
    
    # Get the content of the file
    if GET == '/':
            GET = '/index.html'

    if(GET.find(".html")!=-1):
        try:
            print("Server did it")
            fin = open('htdocs' + GET)
            content = fin.read()
            fin.close()

            # Send HTTP response
            response = 'HTTP/1.0 200 OK\n\n' + content
            client_connection.sendall(response.encode())
            client_connection.close()
        except FileNotFoundError:
            response = 'HTTP/1.0 200 OK\n\n'+'<html><body><h1>404 NOT FOUND</h1>\n\n'+GET+' : File Not Found</body></html>'
            client_connection.sendall(response.encode())
            client_connection.close()