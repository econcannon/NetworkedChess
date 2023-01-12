from mvc.Model.board import Board
from mvc.Model.game import Game
from mvc.View.game_view import GameView
import socket
import pygame
import pickle
import time

class ClientGameController:

    def __init__(self, color, connection) -> None:
        self.color = color
        self.connection = connection
        board = Board(600, 600)
        view = GameView(board, self.color)
        self.game = Game(board, self.color, view)
        pygame.init()


    def start_game(self): 
    
        while True:

            pygame.display.set_caption('Chess')
            self.game.view.display_board(self.color, self.game.board)

            message = False
            while not message:
                message = self.connection.recv(2048).decode()
                if message:
                    self.send_ack(True)
                    break

                else: self.send_ack(False)
            
            message = message.split()
            if message[0] == 'Your':
                self.make_move()

            elif message[0] == 'Move':
                self.receive_and_execute()
                
            elif message[0] == 'Invalid':
                self.make_move()

# Current logic error with empty packets below
            elif message[0] == 'Mate':

                message = False
                while not message:
                    message = self.connection.recv(1024)

                    if message:
                        self.send_ack(True)
                        break
                    else: self.send_ack(False)

                if message:
                    self.game.view.display_winner(True)
                else: self.game.view.display_winner(False)
                return

            elif message[0] == 'Reverse':
                self.game.server_reverse_move()
                self.game.append_all_moves()
                self.make_move()
    
            elif message[0]:
                continue


    def make_move(self):
        """_summary_: 

        """        

        while True:

                cell = self.game.choose_move()

                if not self.game.check_move(self.game.view.has_selected_piece, cell):
                    continue

                cell_val = self.board.get_cell(cell[0], cell[1])

                if cell_val == 0:
                    had_piece = False
                else: had_piece = True

                self.game.server_temp(self.game.view.has_selected_piece, self.game.view.has_selected_piece.location, cell_val, cell, had_piece)
                #updates board info
                self.game.execute_move(self.game.view.has_selected_piece, cell)

                move1 = self.game.view.has_selected_piece.location
                move2 = cell

                self.connection.send(pickle.dumps(move1))
                time.sleep(.1)
                self.connection.send(pickle.dumps(move2))

                #updates list info
                
                #updates attribute info
                self.game.update_piece_location(cell)
                self.game.get_new_moves()
                
                # Wait for the server to check for check condition, then proceed (returns either 1 or 0)
                valid = self.connection.recv(16).decode()
                self.send_ack(True)
                
                if valid:
                    
                    self.game.view.has_selected_piece = False           
                    self.game.view.display_board(self.color, self.game.board)
                    self.game.change_curr_player()
                    break

                else: 
                    
                    self.game.view.display_in_check()
                    if not had_piece:
                        self.game.reverse_move(piece = self.game.view.has_selected_piece, location = self.game.temp_pos, move = cell)
                    else: self.game.reverse_move(self.game.view.has_selected_piece, self.game.temp_pos, self.game.temp_piece, cell)
                    self.game.append_all_moves()
                    self.game.board.update_list()
                    
                    self.game.view.display_in_check()
                    self.game.view.has_selected_piece = False
                    self.game.view.display_board(self.color, self.game.board)
                    continue 


    def send_ack(self, ack: bool):
        """_summary_

        Args:
            ack (bool): Sends a positive (true) or negative (false) acknowledgment to self.connection
            depending on the arg passed
        """        

        if ack:
            ack = '1'.encode()
        else: ack = 'Negative'.encode()

        self.connection.send(ack)

    
    def receive_and_execute(self):
        """_summary_: The receive and execute function includes the entire sequence of 
        client side events from receiving message to updating its board.
        """        

        while True:
            try: 
                message1 = pickle.loads(self.connection.recv(8192))
                message2 = pickle.loads(self.connection.recv(8192))
                        
            except socket.timeout as e:
                self.send_ack(False)
                    
            else:
                if not (message1 and message2):
                    print('Connection error, program shutting down')
                    exit()
                else:
                    self.send_ack(True)
                    break

        piece = self.game.board.get_cell(message1[0], message1[1])
                
        self.game.execute_move(piece, message2)
        # updates attribute info
        self.game.update_piece_location(message2, piece)
        self.game.get_new_moves()
        # updates list info
                
        self.game.view.display_board(self.color, self.game.board)
        self.game.change_curr_player()