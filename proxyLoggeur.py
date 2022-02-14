from socket import *
from datetime import datetime

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5679

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
    request = client_connection.recv(4096).decode()
    dateRequest=datetime.now()
    if(request!=''):
        GET=request.split('\n')[0].split()[1]
        ipHost=request.split('\n')[1]
        if GET == '/':
            GET = '/index.html'
        if(GET.find('.html')!=-1):
            openLog=open('log.txt','a+')
            openLog.writelines('----------------------------------\n')
            openLog.writelines('requête: GET'+GET+'\nadresse ip du '+ipHost)
            openLog.writelines('date et heure de la requête: '+dateRequest.strftime('%Y-%m-%d %H:%M:%S')+'\n')
            openLog.writelines('réponse du serveur: HTTP/1.0'+request.split('HTTP/1.0')[1]+'\n')
            openLog.close()
    client_connection.close()