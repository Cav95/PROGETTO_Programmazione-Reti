# Corso di Programmazione di Reti - Laboratorio - Universit�  di Bologna
# Socket_Programming_Assignment - WebServer - F. Callegati - G.Pau - A. Piroddi

from socket import * 
import os
serverPort=8080
serverSocket = socket(AF_INET, SOCK_STREAM)
server_address=('localhost',serverPort)
serverSocket.bind(server_address)

path = 'www'

#listen(1) Definisce la lunghezza della coda di backlog, ovvero il numero
#di connessioni in entrata che sono state completate dallo stack TCP / IP
#ma non ancora accettate dall'applicazione.
serverSocket.listen(1)
print ('the web server is up on port:',serverPort)

while True:

    print ('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print(connectionSocket,addr)

    try:

        message = connectionSocket.recv(1024)
        if len(message.split())>0: 
            print (message.split()[0],':',message.split()[1]) 
            filename = message.split()[1].decode()
            #filename = '/index.html'
            filepath = os.path.join(path, filename.lstrip('/'))
            print (filename,'||',filename[1:]) 
            
            
            print(filepath)
            f = open(filepath,'rb') 
            outputdata = f.read()
            print (outputdata) 
                
     #Invia la riga di intestazione HTTP nel socket con il messaggio OK

            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            connectionSocket.send(outputdata.encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
            

    except IOError:
 #Invia messaggio di risposta per file non trovato
        connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n","UTF-8"))
        connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
        connectionSocket.close()


