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
            
            print(count)
            # Every loop the count will determine which player makes a move
            if (count%2 == self.first):
                print('Sending turn start code1')
                message = 'Your Turn'.encode()
                self.connection[self.first].send(message)

                while True:

                    # Receive move, check for its validity and update local memory
                    move1 = pickle.loads(self.connection[self.first].recv(1024))
                    move2 = pickle.loads(self.connection[self.first].recv(1024))
                    print(move1, move2)

                    if self.game.current_player == 'b':
                        other_move1 = (7 - move1[0], 7 - move1[1])
                        other_move2 = (7 - move2[0], 7 - move2[1])
                        valid = self.make_move((other_move1, other_move2))
                    else: valid = self.make_move((move1, move2))

                    print('Validity Checked')

                    # If it is a valid move, check for checkmate, then send to opponent
                    if valid:
                        print('Valid Move')
                        if not self.game.check_mate(self.game.other_player):
                            ack = '1'.encode()                        
                            print('Sending', move1, move2)
                            message1 = pickle.dumps(move1)
                            message2 = pickle.dumps(move2)
                            code = 'Move'.encode()
                            self.connection[self.first].send(ack)

                            recv_ack = False
                            while not recv_ack:
                                print('Sending code...')
                                self.connection[(self.first + 1)%2].send(code)
                                time.sleep(.5)
                                print('Sending message1...')
                                self.connection[(self.first + 1)%2].send(message1)
                                time.sleep(.5)
                                print('Sending message2...')
                                self.connection[(self.first + 1)%2].send(message2)
                                time.sleep(2)
                                recv_ack = self.connection[(self.first + 1)%2].recv(1024).decode()

                            print('Move Sent')
                            self.game.change_curr_player()
                            break

                        else: 
                            ack = '1'.encode()                        
                            print('Sending', move1, move2)
                            message1 = pickle.dumps(move1)
                            message2 = pickle.dumps(move2)
                            code = 'Move'.encode()
                            self.connection[self.first].send(ack)

                            recv_ack = False
                            while not recv_ack:
                                print('Sending code...')
                                self.connection[(self.first + 1)%2].send(code)
                                time.sleep(.5)
                                print('Sending message1...')
                                self.connection[(self.first + 1)%2].send(message1)
                                time.sleep(.5)
                                print('Sending message2...')
                                self.connection[(self.first + 1)%2].send(message2)
                                time.sleep(2)
                                recv_ack = self.connection[(self.first + 1)%2].recv(1024).decode()

                            print('Move Sent')
                            first_count += 1
                            self.send_results(first_count)
                            return

                    else:
                        ack = '0'.encode()
                        self.connection[self.first].send(ack)
                print('count incremented')
                count += 1
                first_count += 1

            else:
                print('Sending turn start code2')
                message = 'Your Turn'.encode()
                self.connection[(self.first + 1)%2].send(message)

                while True:

                    # Receive move, check for its validity and update local memory
                    move1 = pickle.loads((self.connection[(self.first + 1)%2].recv(1024)))
                    move2 = pickle.loads((self.connection[(self.first + 1)%2].recv(1024)))
                    print(move1, move2)
                    valid = self.make_move((move1, move2))

                    # If it is a valid move, check for checkmate, then send to opponent
                    if valid:

                        if not self.game.check_mate(self.game.other_player):
                            ack = '1'.encode()
                            print('Sending', move1, move2)
                            message1 = pickle.dumps(move1)
                            message2 = pickle.dumps(move2)
                            code = 'Move'.encode()
                            self.connection[(self.first + 1)%2].send(ack)
                            
                            recv_ack = False
                            while not recv_ack:
                                print('Sending code...')
                                self.connection[self.first].send(code)
                                time.sleep(.5)
                                print('Sending message1...')
                                self.connection[self.first].send(message1)
                                time.sleep(.5)
                                print('Sending message2...')
                                self.connection[self.first].send(message2)
                                time.sleep(2)
                                recv_ack = self.connection[self.first].recv(1024).decode()
                                

                            print('Move Sent')
                            self.game.change_curr_player()
                            break
                        else: 
                            second_count += 1
                            self.send_results(second_count)
                            return

                    else:
                        ack = '0'.encode()
                        self.connection[(self.first + 1)%2].send(ack)
                        
                count += 1
                second_count += 1
            
    
    def send_results(self, count):

        code = 'Mate'.encode()
        message1 = '1'.encode()
        message2 = '0'.encode()
        
        if (count%2 == self.first):
            print('Entered First')
            self.connection[self.first].send(code)
            time.sleep(.1)
            self.connection[(self.first + 1)%2].send(code)
            time.sleep(.1)
            print('Sent', message1)
            self.connection[self.first].send(message1)     
            time.sleep(.1)     
            print('Sent', message2)
            self.connection[(self.first + 1)%2].send(message2)

        else: 
            print('Entered Second')
            self.connection[self.first].send(code)
            time.sleep(.1)
            self.connection[(self.first + 1)%2].send(code)
            time.sleep(.1)
            print('Sent', message2)
            self.connection[self.first].send(message2)    
            time.sleep(.1)      
            print('Sent', message1)
            self.connection[(self.first + 1)%2].send(message1)


    def make_move(self, move):
        """_summary_: Contains the logic of the entire game. Initializes everything, 
                      creates the GUI and checks for win conditions.

        """        
        
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

        print(str(self.game.board))
        
        print(str(self.game.current_player))
        if not self.game.is_in_check(self.game.current_player):
                
            return True

        else: 
                    
            if not had_piece:
                self.game.reverse_move(piece, move[0])
            else: self.game.reverse_move(piece, move[0], cell_val, move[1])
            self.game.append_all_moves()
            print('current player in check')
            return False