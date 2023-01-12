from mvc.Model.board import Board
from mvc.Model.game import Game
import socket
import pickle
import time

class ServerGameController():

    def __init__(self, connection, first) -> None:
        self.connection = connection
        # Allow for server color to be default white for simplicity
        self.color = 'w'
        self.board = Board(600, 600)
        self.game = Game(self.board, self.color)
        self.first = first


    def start_game(self): 
    
        count = self.first
        first_count = 0
        second_count = 0

        while True:
            
            # Every loop the count will determine which player makes a move
            if (count%2 == self.first):
                
                code = 'Your Turn'.encode()
                self.send_code(self.first, code)

                if self.receive_and_execute(self.first, (self.first+1)%2, first_count):
                    return
                
                count += 1
                first_count += 1

            else:

                code = 'Your Turn'.encode()
                self.send_code((self.first+1)%2, code)

                if self.receive_and_execute((self.first+1)%2, self.first, second_count):
                    return
                        
                count += 1
                second_count += 1
            
    
    def send_results(self, count):

        code = 'Mate'.encode()
        message1 = '1'.encode()
        message2 = ''.encode()
        count = str(count).encode()
        
        if (self.game.current_player == 'w'):

            self.send_message(self.first, code, message1)
            self.send_message((self.first + 1)%2, code, message2)
            self.send_message(self.first, code, count)
            self.send_message((self.first + 1)%2, code, count)
            
        else: 

            self.send_message(self.first, code, message2)
            self.send_message((self.first + 1)%2, code, message1)
            self.send_message(self.first, code, count)
            self.send_message((self.first + 1)%2, code, count)


    def make_move(self, move):
        """_summary_: Contains the logic of the entire game. Initializes everything, 
                      creates the GUI and checks for win conditions.

        """        
        print(self.game.current_player, 'moved', move)
        piece = self.game.board.get_cell(move[0][0], move[0][1])
        if not piece:
            return False

        if not self.game.check_move(piece, move[1]):
            return False

        cell_val = self.board.get_cell(move[1][0], move[1][1])

        if cell_val == 0:
            had_piece = False
        else: had_piece = True

        self.game.save_temp(cell_val, move[0])
        # Updates board info
        self.game.execute_move(piece, move[1])
        self.game.board.update_list()
        # Updates attribute info
        self.game.update_piece_location(move[1], piece)
        self.game.get_new_moves()
        self.game.append_all_moves()

        if not self.game.is_in_check(self.game.current_player):
                
            return True

        else: 
                    
            if not had_piece:
                self.game.reverse_move(piece, move[0])
            else: self.game.reverse_move(piece, move[0], cell_val, move[1])
            print('current player in check')
            return False

    
    def send_message(self, connection, code, message1 = 0,  message2 = 0):
        recv_ack = False
        t_count = 0
        while not recv_ack:
            
            self.send_code(connection, code)
            if message1:
                self.connection[connection].send(message1)
                time.sleep(.1)
            if message2: 
                self.connection[connection].send(message2)

            try:
                recv_ack = self.connection[connection].recv(1024).decode()
                if recv_ack == 'Negative':
                    continue
                                
            except TimeoutError as e:
                t_count += 1
                print('Waiting for client acknowledgment')
                if t_count < 4:
                    continue
                else: 
                    print('No ack received, program exiting')
                    exit()

            else: 
                if not recv_ack:
                    print('Connection error occurred, program exiting')
                    exit()

    
    def send_code(self, connection, code):

        recv_ack = False
        t_count = 0
        while not recv_ack:
            
            try:
                self.connection[connection].send(code)
                if recv_ack == 'Negative':
                    continue

            except TimeoutError as e:
                    t_count += 1
                    print('Waiting for client acknowledgment')
                    if t_count < 4:
                        continue
                    else: 
                        print('No ack received, program exiting')
                        exit()

            else: 
                if not recv_ack:
                    print('Connection error occurred, program exiting')
                    exit()

    
    def receive_and_execute(self, first, second, count):
        # First is the current player, the one that is expected to make the move
        # Second is the other player, the one that will receive the message

        while True:

            # Receive move, check for its validity and update local memory
            move1 = pickle.loads(self.connection[first].recv(1024))
            move2 = pickle.loads(self.connection[first].recv(1024))

            valid = self.make_move((move1, move2))
            print(valid)
            # If it is a valid move, check for checkmate, then send to opponent
            if valid:
                
                check = self.game.check_mate(self.game.other_player)
                

                ack = '1'.encode()                        
                print('Sending', move1, move2)
                message1 = pickle.dumps(move1)
                message2 = pickle.dumps(move2)
                code = 'Move'.encode()
                self.connection[first].send(ack)

                self.send_message(second, code, message1, message2)
                          
                self.game.change_curr_player()
                    
                if check:
                    self.send_results(count)
                    return True
                else:
                    return False
            else:
                ack = 'Reverse'.encode()
                self.connection[first].send(ack)