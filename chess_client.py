# This file is intended to initialize the client side of the chess game


from socket import *

class Chess_Client():
    
    def __init__(self) -> None:
        
        # Initialize variables
        server_address = '192.168.2.240'
        server_port_number = 12001
        server_identifier = ( server_address , server_port_number )

        # Create client socket
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        # Connect to the Server
        self.client_socket.connect(server_identifier)

        # Wait for user to send their color
        print('Waiting for opponent to choose color...')
        other_color = self.client_socket.recv(1024)

        # Determine local color
        if other_color == 'w':
            self.color = 'b'
            print('Opponent chose white, you are black')
        else: 
            self.color = 'w'
            print('Opponent chose black, you are white')
        

    def send_move(self, board):

        self.client_socket.send(board.encode())

    
    def receive_move(self):

        return self.client_socket.recv(2048).decode()  
          
    
    def disconnect(self):

        self.client_socket.close()