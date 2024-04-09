import threading
from concurrent.futures import ThreadPoolExecutor

import os 
from networking.socket_utils import SocketUtils

# Start the server
server_address = ('localhost', 10000)

# Create socket from the server address
sock = SocketUtils.create_socket(server_address)

# Open thread pool 
workers = 100
executor = ThreadPoolExecutor(max_workers=workers) # can handle 100 concurrent connections

def handle_client(connection):
    try:
        while True:
            # Recieve data from client and process data 
            data = SocketUtils.receive_data(connection)
            if data:
                # Send response back to client 
                SocketUtils.send_data(connection, data)
            else:
                break
    finally:
        # close connection 
        SocketUtils.close_connection(connection)

def accept_clients():
    try:
        while True:
            connection, client_address = SocketUtils.accept_connection(sock) # accept connection from client app 
            executor.submit(handle_client, connection) # submit connection to thread pool
    except Exception as e:
        print(f"Error accepting clients: {e}")

# Start accepting clients
accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()

# Wait for the accept_thread to finish
accept_thread.join()