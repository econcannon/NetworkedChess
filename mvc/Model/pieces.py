from abc import ABC, abstractmethod
import pygame


white = []
black = []

#Move to proper file later
#pygame.display()

#black pieces
black_pawn_img = pygame.image.load('mvc\\Model\\Imgs\\black_pawn.png')
black_knight_img = pygame.image.load('mvc\\Model\\Imgs\\black_knight.png')
black_bishop_img = pygame.image.load('mvc\\Model\\Imgs\\black_bishop.png')
black_queen_img = pygame.image.load('mvc\\Model\\Imgs\\black_queen.png')
black_king_img = pygame.image.load('mvc\\Model\\Imgs\\black_king.png')
black_rook_img = pygame.image.load('mvc\\Model\\Imgs\\black_rook.png')

#white pieces
white_pawn_img = pygame.image.load('mvc\\Model\\Imgs\\white_pawn.png')
white_rook_img = pygame.image.load('mvc\\Model\\Imgs\\white_rook.png')
white_knight_img = pygame.image.load('mvc\\Model\\Imgs\\white_knight.png')
white_bishop_img = pygame.image.load('mvc\\Model\\Imgs\\white_bishop.png')
white_queen_img = pygame.image.load('mvc\\Model\\Imgs\\white_queen.png')
white_king_img = pygame.image.load('mvc\\Model\\Imgs\\white_king.png')


white = [white_pawn_img, white_rook_img, white_knight_img, white_bishop_img, white_queen_img, white_king_img]
black = [black_pawn_img, black_rook_img, black_knight_img, black_bishop_img, black_queen_img, black_king_img]

block_w, block_h = 600/8, 600/8

for img in white:
    pygame.transform.scale(img, (block_w*1/2, block_h*3/4))
for img in black:
    pygame.transform.scale(img, (block_w*1/2, block_h*3/4))




class Pieces(ABC):

    def __init__(self, color, location: tuple):
        self.color = color
        self.location = location
        #self.draw
        self.moves = []
        #self.other_location = (7 - location[0], 7 - location[1])
        
#for objects of certain color in pieces, check moves if move overlaps king position, king in check
    def valid_move(self, board):
        for move in self.moves:

            #check border of board
            if (move[0] < 0) or (move[1]) < 0:
                self.moves.remove(move)
            elif (move[0] > 8) or (move[1] > 8):
                self.moves.remove(move)
            
            #check if cell contains piece of own color
            if board.get_cell(move[0][1]).color == self.color:
                self.moves.remove(move)


    def update_location(self, location):
        self.location[0], self.location[1] = location[0], location[1]
        self.other_location[0], self.other_location[1] = 7 - location[0], 7 - location[1]


    #def draw_img(self, win):
    #   if self.color == 'b':
    #       img = black[self.img]
    #   elif self.color == 'w':
    #       img = white[self.img]

    #   x, y = self.location[0]*1/4, self.location[1]*1/8
    #   win.blit(img, (x,y))

    