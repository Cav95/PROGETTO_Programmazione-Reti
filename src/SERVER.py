from socket import *
import os

serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
server_address = ('localhost', serverPort)
serverSocket.bind(server_address)

script_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_dir, 'www')

serverSocket.listen(1)
print('the web server is up on port:', serverPort)

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode('utf-8')

        if len(message.split()) > 1:
            http_method = message.split()[0]
            requested_file = message.split()[1]

            filename = requested_file.lstrip('/')
            filepath = os.path.join(path, filename)

            with open(filepath, 'rb') as f:
                outputdata = f.read()

            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode('utf-8'))
            connectionSocket.send("\r\n".encode('utf-8'))
            connectionSocket.send(outputdata)
            connectionSocket.close()

        else:
            connectionSocket.send(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            connectionSocket.send(b"<html><head></head><body><h1>400 Bad Request</h1></body></html>\r\n")
            connectionSocket.close()

    except FileNotFoundError:
        print(f"ERRORE: File non trovato: {filepath}")
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
        connectionSocket.close()