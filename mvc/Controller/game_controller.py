from mvc.Model.board import Board
from mvc.Model.game import Game
from mvc.View.game_view import GameView
import pygame

class GameController:

    def __init__(self, color, connection) -> None:
        self.color = color
        self.connection = connection
        self.board = Board(600, 600)
        self.view = GameView(self.board, self.color)
        self.game = Game(self.board, self.view, self.color)


    def start_game(self): 
    
        count = 0

        while not self.game.check_mate():

            pygame.display.set_caption('Chess')
            self.view.display_board(self.color)

            # Every loop the count will determine which player makes a move
            if (self.color == 'w') and (count%2 == 0):
                self.make_move()
                self.connection.send_move(self.game.board)
                count += 1

            else: 
                move = self.connection.receive_move()
                self.game.update_board(move)
                count += 1
            

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

                self.game.save_temp(cell_val, self.view.has_selected_piece.location)
                #updates board info
                self.game.execute_move(self.view.has_selected_piece, cell)
                #updates list info
                self.view.board.update_list()
                #updates attribute info
                self.game.update_piece_location(cell)
                self.game.get_new_moves()
                

                if not self.game.is_in_check():
                    
                    self.view.has_selected_piece = False           
                    self.view.display_board(self.color)
                    self.game.change_curr_player()
                    break

                else: 
                    
                    self.view.display_in_check()
                    if not had_piece:
                        self.game.reverse_move(piece = self.view.has_selected_piece, location = self.game.temp_pos, move = cell)
                    #1st arg is piece that was just moved
                    #2nd arg is piece that was captured
                    #3rd arg is position of piece from arg 1
                    #4th arg is position of captured piece
                    else: self.game.reverse_move(self.view.has_selected_piece, self.game.temp_pos, self.game.temp_piece, cell)
                    self.game.append_all_moves()
                    self.view.board.update_list()
                    self.view.display_in_check()
                    self.view.has_selected_piece = False
                    continue 

                
        winner = self.game.get_winner()
        self.view.display_winner(winner)
        pygame.time.delay(7000)
        pygame.quit()