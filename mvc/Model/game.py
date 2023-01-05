from mvc.Model.player import Player
from mvc.View.game_view import GameView
from mvc.Model.board import Board
import pygame
from pygame.locals import *

class Game:
    EMPTY = int(0)

    def __init__(self, board: Board, color, view: GameView = 0) -> None:

        self.color = color
        self.view = view
        self.current_player = Player.White
        self.other_player = Player.Black
        self.board = board
        self.turn = 0
        self.temp_piece = 0
        self.temp_pos = (0, 0)
        self.winner = 0

    def choose_move(self):
        # Need this to return both the position that the selected piece is in as well as the position it is moving to
        while True:
            
            pygame.display.update()
            mx, my = pygame.mouse.get_pos()
            row, col = int(my/self.view.block_height), int(mx/self.view.block_width)
                        
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
        
                    if event.button == 1:
                        pos = (row, col)
                        if self.current_player == 'b':
                            pos = (7 - pos[0], 7 - pos[1])

                        cell = self.board.get_cell(pos[0], pos[1])
                        if cell == 0:
                            if self.view.has_selected_piece:
                                return pos
                            #else do nothing, because, no reason to select empty cell without selected piece

                        else: 
                            if cell.color == self.current_player:

                                if self.view.has_selected_piece:

                                    self.view.is_selected_piece(cell)
                                    
                                    if self.current_player == 'b':
                                        self.view.display_reverse_block()
                                        
                                    else: 
                                        self.view.display_block_border()

                                    self.view.display_board(self.color)
                                        
                                else: 
                                    self.view.is_selected_piece(cell)
                                    if self.current_player == 'b':
                                        self.view.display_reverse_block()
                                        
                                    else: 
                                        self.view.display_block_border()

                            else:
                                if self.view.has_selected_piece:
                                    return pos
                                #else do nothing, because, no reason to select opponent piece without selected piece  

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 
        
    
    def get_new_moves(self):
        """_summary_: Deletes the moves of every piece in the game and finds their new moves
        """        
        
            #Deletes prior move possibilities
        for piece in self.board.pieces_lst:
            piece.moves = []
            #Finds moves based on new position
            piece.append_moves(self.board)


    def check_move(self, piece, move):
        """_summary_: Takes a piece and a move and determines if the move is contained by that piece's possible moves

        Args:
            piece (_type_): The piece whose moves will be checked
            move (_type_): The move which will be compared to the piece.moves list

        Returns:
            _type_: Boolean return of whether or not the movement is allowed by that piece type
        """        

        piece.append_moves(self.board)
        if move in piece.moves:

            return True
        else: return False

    

    def execute_move(self, piece, location):
        """_summary_: Given a piece and a move location, transfers piece information to that location in the matrix,
                      and deletes the piece information from the prior location

        Args:
            piece (_type_): The piece to be moved
            location (_type_): The location for the piece to be moved to
        """        

        if self.board.get_cell(location[0], location[1]) != 0:
            captured = self.board.get_cell(location[0], location[1])
            self.capture_piece(captured)

        self.remove_piece(piece.location)
        self.board.set_cell(piece, location[0], location[1])
        
        if str(piece) == 'King':
            if piece.color == 'b':
                self.board.black_king_pos = location
            else: self.board.white_king_pos = location
        piece.turn += 1


    def save_temp(self, piece, location):

        self.temp_piece = piece
        self.temp_pos = location


    def server_temp(self, piece, location, other_piece, other_location, had_piece):
        """_summary_: When checking movements validity for checking if player in check, saving the pieces
                      information and location is necessary to reverse the move when necessary.
                      The lost information when moving is the moved piece's prior location, and the piece being captured

        Args:
            piece (_type_): The value of the cell which the piece is being moved to. Could contain a piece, or could be empty
            location (_type_): The location from which the piece is being moved.
        """        
        self.temp_pos1 = location
        self.temp_piece1 = piece
        self.temp_pos2 = other_location
        self.temp_piece2 = other_piece
        self.temp_had_piece = had_piece


    def reverse_move(self, piece, location, other = 0, move = 0):
        """_summary_: In the event that a move results in a player being in check, the move must be reversed
                      This function reverses the pieces location attributes, the matrix data, and the captured piece,
                      and the boards pieces_list attribute

        Args:
            piece (_type_): The piece that was moved
            location (_type_): location of piece from arg 1 before movement
            other (int, optional): the piece that was captured if applicable
            move (int, optional): the location of the piece that was captured if applicable
        """

        if other:
            
            piece.turn -= 1
            #restores location attribute
            piece.location = location
            if str(piece) == 'King':
                if piece.color == 'b':
                    self.board.black_king_pos = location
                else: self.board.white_king_pos = location
            #restores moved piece in board
            self.board.set_cell(piece, location[0], location[1])
            self.remove_piece(move)
            #restores captured piece
            self.board.set_cell(other, move[0], move[1])
            #restores list 
            self.board.pieces_lst.append(other)
            if self.view:
                self.view.display_board(self.color)

        else: 
            piece.turn -= 1
            #restore attribute
            piece.location = location
            #restore board
            self.board.set_cell(piece, location[0], location[1])
            self.remove_piece(piece.location)
            if self.view:
                self.view.display_board(self.color)


    def remove_piece(self, location):
        """_summary_: removes the piece from the board

        Args:
            location (_type_): the location of the piece which is being removed
        """        

        self.board.board[location[0]][location[1]] = self.EMPTY


    def capture_piece(self, piece):
        """_summary_: when a piece is captured, this function removes the piece from the board and removes it 
                      from the board pieces_list attribute

        Args:
            piece (_type_): the piece which is being captured
        """        

        self.remove_piece(piece.location)
        self.board.pieces_lst.remove(piece)


    def change_curr_player(self):
        """_summary_: updates the current player
        """        

        if self.current_player == Player.White:
            self.current_player = Player.Black
            self.other_player = Player.White
        else: 
            self.current_player = Player.White
            self.other_player = Player.Black


    def is_in_check(self, color):
        """_summary_: Determines if the current player is in check by going through each of the opponent's
                      piece's moves and determining if the kings loation is within one of the moves.

        Returns:
            _type_: Boolean true if in check, false if not
        """        

        black_king_loc = self.board.black_king_pos
        white_king_loc = self.board.white_king_pos

        #append each pieces moves to ensure updated
        for piece in self.board.pieces_lst:

            piece.append_moves(self.board)

        #once all moves are appended, see if in check
        for piece in self.board.pieces_lst:

            if color == 'w':

                if piece.color == 'w':
                    continue

                if piece.color == 'b':

                    if white_king_loc in piece.moves:
                        print('IS IN CHECK')
                        return True
                        
                    else: continue
            
            else:

                if piece.color == 'w':
            
                    if black_king_loc in piece.moves:
                        print('IS IN CHECK')
                        return True
                        
                    else: continue

                if piece.color == 'b':
                    continue

        return False
                

    def check_mate(self, color):
        """_summary_: Determines if the current player is in check and then if there is any possible move to 
        get out of check. Done by executing and subsequently reversing every move possible and checking if in check
        after move has been made.

        Returns:
            _type_: Boolean return of true if checkmate, false if move to get out of check exists.
        """        

        if not self.is_in_check(color):
            
            return False

        else:
            for piece in self.board.pieces_lst:
                
                if color == piece.color:

                    for move in piece.moves:
                        
                        move_val = self.board.get_cell(move[0], move[1])

                        if move_val == 0:
                            had_piece = False
                        else: had_piece = True

                        self.save_temp(move_val, piece.location)
                        #updates board info
                        self.execute_move(piece, move)
                        #updates list info
                        
                        self.board.update_list()
                        #updates attribute info
                        self.update_piece_location(move, piece)
                        self.get_new_moves()
                        
                        if not self.is_in_check(color):
                            
                            if not had_piece:
                                self.reverse_move(piece = piece, location = self.temp_pos, move = move)

                            else: 
                                self.reverse_move(piece, self.temp_pos, self.temp_piece, move)

                            self.get_new_moves()
                            return False

                        else: 

                            if not had_piece:
                                self.reverse_move(piece = piece, location = self.temp_pos, move = move)
                                
                            else: 
                                self.reverse_move(piece, self.temp_pos, self.temp_piece, move)
                            
                            self.get_new_moves()
                            continue
            print('check mate')
            return True

                    
    def get_winner(self):
        """:Once a player has won, returns which player was victorious

        Returns:
            _type_: the player that won
        """        
        
        return self.other_player


    def update_piece_location(self, location, piece = 0):
        """: updates a pieces attributes to its new location. If piece is passed as argument, changes location of 
        selected piece, if not, changes location of the piece that has been selected previously

        Args:
            location (_type_): the location to update the piece's attributes to
            piece (int, optional): the piece whose location is to be updated. Defaults to 0.
        """        
        
        if not piece:
            self.view.has_selected_piece.location = location
        else: piece.location = location

    
    def append_all_moves(self):
        """_summary_: Deletes the moves of every piece in the game and finds their new moves
        """        
        for piece in self.board.pieces_lst:
            piece.append_moves(self.board)

    
    def update_board(self, move):
        
        self.board = move
        self.board.update_list()
        self.append_all_moves()

    
    def server_reverse_move(self):
        if not self.temp_had_piece:
            self.reverse_move(self.temp_piece1, self.temp_pos1, self.temp_piece2, self.temp_pos2)
        else: self.reverse_move(self.temp_piece1, self.temp_pos1)