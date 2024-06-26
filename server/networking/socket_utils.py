import socket 
import sys 
from service.processing import ProcessingService

class SocketUtils: 
    
    @classmethod 
    def create_socket(cls, server_address):
        print('Listening on %s port %s' % server_address, file=sys.stderr)
        # Create a TCP socket. Currently supports IPv4 but can expand to IPv6 if needed
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(server_address)
        # This is the backlog parameter, specifies max # of pending connections that can be queued up before the server starts 
        # rejecting new connection requests.  
        sock.listen(1)
        return sock

    @classmethod
    def accept_connection(cls, sock):
        connection, client_address = sock.accept()
        return connection, client_address

    @classmethod
    def send_data(cls, connection, data):
        print('sending "%s"' % data, file=sys.stderr)
        connection.sendall(data)

    @classmethod
    def receive_data(cls, connection, size=266):
        try: 
            data = connection.recv(size) # receive data from client
            if(data!=b''):
                print('received "%s"' % data, file=sys.stderr)
                res = ProcessingService().process(data, None) # Process data for insertion or retrieval
                return res # return data to client
        except Exception as e: 
            print(e)
            return None 

    @classmethod
    def close_connection(cls, connection): # close connection 
        connection.close()