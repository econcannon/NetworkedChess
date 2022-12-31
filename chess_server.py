# This file is intended to initialize the server of the game


from socket import *


class Chess_Server():

    def __init__(self) -> None:
        

        # Initialize variables
        address = 'localhost'
        port_number = 12000
        identifier = (address, port_number)

        # Create and bind Server Soceket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(identifier)

        self.server_socket.listen(1)
        print('Server listening for connection')

        self.connection_socket, client_address = self.server_socket.accept()
        print('Connection created at %d', client_address)
        
        # Server side chooses player color
        while True:
            print('Choose your color')
            self.color = input('Enter \'w\' or \'b\'')

            if (self.color == 'w') or (self.color == 'b'):
                break
            else: print('Invalid Input, please try again...')

        self.connection_socket.send(self.color)
        


    def send_move(self, board):

        self.connection_socket.send(board)

    
    def receive_move(self):

        return self.connection_socket.recv(2048)  