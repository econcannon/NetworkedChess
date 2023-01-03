from mvc.Model.board import Board
from mvc.Model.game import Game
from mvc.View.game_view import GameView
import pygame
import pickle
import time

class ClientGameController:

    def __init__(self, color, connection) -> None:
        self.color = color
        self.connection = connection
        self.board = Board(600, 600)
        self.view = GameView(self.board, self.color)
        self.game = Game(self.board, self.color, self.view)
        pygame.init()


    def start_game(self): 
    
        while True:

            pygame.display.set_caption('Chess')
            self.view.display_board(self.color)

            message = self.connection.recv(2048).decode()
            print(message)
            message = message.split()

            if message[0] == 'Your':
                self.make_move()

            elif message[0] == 'Move':
                message1 = pickle.loads(self.connection.recv(8192))
                message2 = pickle.loads(self.connection.recv(8192))
                print('Received', message1, message2)
                piece = self.game.board.get_cell(message1[0], message1[1])
                print(str(piece))
                self.game.execute_move(piece, message2)
                #updates attribute info
                self.game.update_piece_location(message2, piece)
                self.game.get_new_moves()
                #updates list info
                self.view.board.update_list()
                print(str(self.game.board))
                self.game.change_curr_player()
                
            elif message[0] == 'Invalid':
                self.make_move()

            elif message[0] == 'Winner!':
                self.view.display_winner(True)

            elif message[1] == 'Loser...':
                self.view.display_winner(False)

            elif message:
                continue

            elif not message:
                self.game.server_reverse_move()
                self.game.append_all_moves()
                self.view.board.update_list()
                self.make_move()


    def make_move(self):
        """_summary_: Contains the logic of the entire game. Initializes everything, 
                      creates the GUI and checks for win conditions.

        """        

        
        while True:

                cell = self.game.choose_move()

                if not self.game.check_move(self.view.has_selected_piece, cell):
                    continue

                cell_val = self.board.get_cell(cell[0], cell[1])

                if cell_val == 0:
                    had_piece = False
                else: had_piece = True

                self.game.server_temp(self.view.has_selected_piece, self.view.has_selected_piece.location, cell_val, cell, had_piece)
                #updates board info
                self.game.execute_move(self.view.has_selected_piece, cell)

                move1 = self.view.has_selected_piece.location
                move2 = cell

                self.connection.send(pickle.dumps(move1))
                time.sleep(.01)
                self.connection.send(pickle.dumps(move2))
                print('Move Sent')

                #updates list info
                self.view.board.update_list()
                #updates attribute info
                self.game.update_piece_location(cell)
                self.game.get_new_moves()
                
                # Wait for the server to check for check condition, then proceed (returns either 1 or 0)
                valid = self.connection.recv(16).decode()
                
                if valid:
                    
                    self.view.has_selected_piece = False           
                    self.view.display_board(self.color)
                    self.game.change_curr_player()
                    break

                else: 
                    
                    self.view.display_in_check()
                    if not had_piece:
                        self.game.reverse_move(piece = self.view.has_selected_piece, location = self.game.temp_pos, move = cell)
                    else: self.game.reverse_move(self.view.has_selected_piece, self.game.temp_pos, self.game.temp_piece, cell)
                    self.game.append_all_moves()
                    self.view.board.update_list()
                    self.view.display_in_check()
                    self.view.has_selected_piece = False
                    continue 
        
                
        #winner = self.game.get_winner()
        #self.view.display_winner(winner)
        #pygame.time.delay(7000)
        #pygame.quit()
        #self.connection.close()