from mvc.Model.bishop import Bishop
from mvc.Model.pawn import Pawn
from mvc.Model.rook import Rook
from mvc.Model.queen import Queen
from mvc.Model.king import King
from mvc.Model.knight import Knight

import pygame


class Board:


    def __init__(self, screen_h, screen_w) -> None:
        EMPTY = int(0)
        self.screen_h = screen_h
        self.screen_w = screen_w
        self.block_h, self.block_w = screen_h/8, screen_w/8

        board = []
        board = [[EMPTY for i in range(8)] for j in range(8)]

        board[0][0] = Rook('b', (0,0))
        board[0][1] = Knight('b', (0,1))
        board[0][2] = Bishop('b', (0,2))
        board[0][3] = Queen('b', (0,3))
        board[0][4] = King('b', (0,4))
        board[0][5] = Bishop('b', (0,5))
        board[0][6] = Knight('b', (0,6))
        board[0][7] = Rook('b', (0,7))

        board[1][0] = Pawn('b', (1,0))
        board[1][1] = Pawn('b', (1,1))
        board[1][2] = Pawn('b', (1,2))
        board[1][3] = Pawn('b', (1,3))
        board[1][4] = Pawn('b', (1,4))
        board[1][5] = Pawn('b', (1,5))
        board[1][6] = Pawn('b', (1,6))
        board[1][7] = Pawn('b', (1,7))

        board[7][0] = Rook('w', (7,0))
        board[7][1] = Knight('w', (7,1))
        board[7][2] = Bishop('w', (7,2))
        board[7][3] = Queen('w', (7,3))
        board[7][4] = King('w', (7,4))
        board[7][5] = Bishop('w', (7,5))
        board[7][6] = Knight('w', (7,6))
        board[7][7] = Rook('w', (7,7))

        board[6][0] = Pawn('w', (6,0))
        board[6][1] = Pawn('w', (6,1))
        board[6][2] = Pawn('w', (6,2))
        board[6][3] = Pawn('w', (6,3))
        board[6][4] = Pawn('w', (6,4))
        board[6][5] = Pawn('w', (6,5))
        board[6][6] = Pawn('w', (6,6))
        board[6][7] = Pawn('w', (6,7))

        self.pieces_lst = []
        self.board = board
        self.set_list()
        
        self.black_king_pos = (0, 4)
        self.white_king_pos = (7, 4)

        img = pygame.image.load('mvc\\Model\\Imgs\\chess_board_img.png')
        img = pygame.transform.scale(img, (self.screen_h, self.screen_w))
        self.img = img
     

    def __str__(self):
        first = [str(x) for x in self.board[0]]
        sec = [str(x) for x in self.board[1]]
        third = [str(x) for x in self.board[2]]
        fourth = [str(x) for x in self.board[3]]
        fifth = [str(x) for x in self.board[4]]
        sixth = [str(x) for x in self.board[5]]
        seventh = [str(x) for x in self.board[6]]
        eigth = [str(x) for x in self.board[7]]
        disp_bo = [first, sec, third, fourth, fifth, sixth, seventh, eigth]

        return f'{disp_bo[0]}\n{disp_bo[1]}\n{disp_bo[2]}\n{disp_bo[3]}\n{disp_bo[4]}\n{disp_bo[5]}\n{disp_bo[6]}\n{disp_bo[7]}'


    def get_cell(self, row, col):
        """_summary_: Determines the value of the cell at location determined by row and col

        Args:
            row (_type_): Row to be checked
            col (_type_): Column to be checked

        Returns:
            _type_: cell value
        """        
        return self.board[row][col]

    
    def set_cell(self, piece, row, col):
        """_summary_: Sets the value of a cell

        Args:
            piece (_type_): the piece to be set in a location
            row (_type_): the row to place the piece in
            col (_type_): the col to place the piece in
        """        
        self.board[row][col] = piece

    
    def set_list(self):
        """_summary_: Sets initial values of board list attribute
        """        

        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                if self.board[x][y] != 0:
                    self.pieces_lst.append(self.board[x][y])

    
    def update_list(self):
        """_summary_: Updates the value of the board list attribute
        """        

        self.pieces_lst = []
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                if self.board[x][y] != 0: 
                    self.pieces_lst.append(self.board[x][y])
                