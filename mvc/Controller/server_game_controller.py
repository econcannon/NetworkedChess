from mvc.Model.board import Board
from mvc.Model.game import Game
import socket
import pickle

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

        while True:
            
            # Every loop the count will determine which player makes a move
            if (count%2 == self.first):
                message = 'Your Turn'.encode()
                self.connection[self.first].send(message)

                while True:

                    # Receive move, check for its validity and update local memory
                    move = pickle.loads(self.connection[self.first].recv(1024))
                    move = move.split()
                    valid = self.make_move(move)

                    # If it is a valid move, check for checkmate, then send to opponent
                    if valid:

                        if not self.game.check_mate():
                            ack = '1'.encode()
                            message = pickle.dumps(move)
                            code = 'Move'.encode()
                            self.connection[self.first].send(ack)
                            self.connection[(self.first + 1)%2].send(code)
                            self.connection[(self.first + 1)%2].send(message)
                            break
                        else: 
                            self.send_results(count)
                            return

                    else:
                        ack = '0'.encode()
                        self.connection[self.first].send(ack)

                count += 1

            else:
                message = 'Your Turn'.encode()
                self.connection[(self.first + 1)%2].send(message)

                while True:

                    # Receive move, check for its validity and update local memory
                    move = pickle.loads(self.connection[(self.first + 1)%2].recv(1024))
                    valid = self.make_move(move)

                    # If it is a valid move, check for checkmate, then send to opponent
                    if valid:

                        if not self.game.check_mate():
                            ack = '1'.encode()
                            message = pickle.dumps(move)
                            code = 'Move'.encode()
                            self.connection[(self.first + 1)%2].send(ack)
                            self.connection[self.first].send(message)
                            self.connection[self.first].send(code)
                            break
                        else: 
                            self.send_results(count)
                            return

                    else:
                        ack = '0'.encode()
                        self.connection[(self.first + 1)%2].send(ack)
                        
                count += 1
            
    
    def send_results(self, count):

        message1 = f'Winner! in {count/2} moves'.encode()
        message2 = f'Loser... in {count/2} moves'.encode()
        
        if (count%2 == self.first):
            
            self.connection[self.first].send(message1)          
            self.connection[(self.first + 1)%2].send(message2)

        else: 

            self.connection[self.first].send(message2)          
            self.connection[(self.first + 1)%2].send(message1)


    def make_move(self, move):
        """_summary_: Contains the logic of the entire game. Initializes everything, 
                      creates the GUI and checks for win conditions.

        """        
        
        piece = self.game.board.get_cell(move[0][0], move[0][1])
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
                
        if not self.game.is_in_check():
                
            return True

        else: 
                    
            if not had_piece:
                self.game.reverse_move(piece, move[0])
            else: self.game.reverse_move(piece, move[0], cell_val, move[1])
            self.game.append_all_moves()
            return False