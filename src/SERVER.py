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
    print(f"Connessione da: {addr}")

    try:
        message = connectionSocket.recv(1024).decode('utf-8')
        print(f"Messaggio ricevuto: {message.strip()}") # Stampa il messaggio completo per debug

        if len(message.split()) > 1:
            http_method = message.split()[0]
            requested_file = message.split()[1]

            print(f"Analisi richiesta - Metodo: {http_method}, File: {requested_file}")

            # Rimuovi lo slash iniziale dal nome del file se presente
            filename = requested_file.lstrip('/')

            # Costruisci il percorso completo al file
            filepath = os.path.join(path, filename)

            with open(filepath, 'rb') as f:
                outputdata = f.read()

            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode('utf-8'))

        # Aggiungi un'intestazione Content-Type in base all'estensione del file
            if filename.endswith('.html'):
                connectionSocket.send("Content-Type: text/html\r\n".encode('utf-8'))
            elif filename.endswith('.css'):
                connectionSocket.send("Content-Type: text/css\r\n".encode('utf-8'))
            elif filename.endswith('.js'):
                connectionSocket.send("Content-Type: application/javascript\r\n".encode('utf-8'))
            elif filename.endswith(('.jpg', '.jpeg')):
                connectionSocket.send("Content-Type: image/jpeg\r\n".encode('utf-8'))
            elif filename.endswith('.png'):
                connectionSocket.send("Content-Type: image/png\r\n".encode('utf-8'))
            else:
                connectionSocket.send("Content-Type: application/octet-stream\r\n".encode('utf-8'))

            connectionSocket.send("\r\n".encode('utf-8'))
            connectionSocket.send(outputdata)

            connectionSocket.close()
            print("Richiesta servita e connessione chiusa.")

        else:
            print("Richiesta HTTP malformata o vuota ricevuta.")
            connectionSocket.send(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            connectionSocket.send(b"<html><head></head><body><h1>400 Bad Request</h1></body></html>\r\n")
            connectionSocket.close()


    except FileNotFoundError: # Cattura specificamente FileNotFoundError
        print(f"ERRORE: File non trovato: {filepath}")
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
        connectionSocket.close()
    except IOError as e: # Cattura altri errori I/O (es. permessi)
        print(f"ERRORE I/O generico durante l'apertura del file {filepath}: {e}")
        connectionSocket.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        connectionSocket.send(b"<html><head></head><body><h1>500 Internal Server Error</h1></body></html>\r\n")
        connectionSocket.close()
    except Exception as e:
        print(f"ERRORE inaspettato durante il servizio della richiesta: {e}")
        connectionSocket.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        connectionSocket.send(b"<html><head></head><body><h1>500 Internal Server Error</h1></body></html>\r\n")
        connectionSocket.close()