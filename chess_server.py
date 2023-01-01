# This file is intended to initialize the server of the game


import socket


class Chess_Server():

    def __init__(self) -> None:
        

        # Initialize variables
        HOST = ''
        PORT = 12002
        IDENTIFIER = (HOST, PORT)

        # Create and bind Server Soceket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Host socket created...')
            
        self.server_socket.bind(IDENTIFIER)

        # Change default timeout
        self.server_socket.settimeout(15)

        print('Server listening for connection...')
        self.server_socket.listen(1)
            
        self.connection_socket, client_address = self.server_socket.accept()
        
        print('Connection created at', client_address)
                        
        # Server side chooses player color
        while True:
            print('Choose your color')
            self.color = input('Enter \'w\' or \'b\'')

            if (self.color == 'w') or (self.color == 'b'):
                break
            else: print('Invalid Input, please try again...')

        self.connection_socket.send(self.color.encode())
                


    def send_move(self, board):

        self.connection_socket.send(board.encode())

    
    def receive_move(self):

        return self.connection_socket.recv(2048).decode() 


    def disconnect(self):

        self.connection_socket.close() 
        self.server_socket.close()