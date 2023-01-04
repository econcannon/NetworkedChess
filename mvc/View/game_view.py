import pygame
from pygame.locals import *

class GameView:

    def __init__(self, board, color) -> None:
        
        self.color = color
        self.board = board
        self.screen_height, self.screen_width = 600, 600
        self.block_height, self.block_width = self.screen_height/8, self.screen_width/8

        self.window = pygame.display.set_mode((self.screen_height, self.screen_width))
        pygame.display.set_caption('Chess')
        

        #black pieces
        black_pawn_img = pygame.image.load('mvc\\Model\\Imgs\\black_pawn.png')
        black_rook_img = pygame.image.load('mvc\\Model\\Imgs\\black_rook.png')
        black_knight_img = pygame.image.load('mvc\\Model\\Imgs\\black_knight.png')
        black_bishop_img = pygame.image.load('mvc\\Model\\Imgs\\black_bishop.png')
        black_queen_img = pygame.image.load('mvc\\Model\\Imgs\\black_queen.png')
        black_king_img = pygame.image.load('mvc\\Model\\Imgs\\black_king.png')

        #white pieces
        white_pawn_img = pygame.image.load('mvc\\Model\\Imgs\\white_pawn.png')
        white_rook_img = pygame.image.load('mvc\\Model\\Imgs\\white_rook.png')
        white_knight_img = pygame.image.load('mvc\\Model\\Imgs\\white_knight.png')
        white_bishop_img = pygame.image.load('mvc\\Model\\Imgs\\white_bishop.png')
        white_queen_img = pygame.image.load('mvc\\Model\\Imgs\\white_queen.png')
        white_king_img = pygame.image.load('mvc\\Model\\Imgs\\white_king.png')

        #white piece scale
        white_pawn_img = pygame.transform.scale(white_pawn_img, (self.block_width*1/2, self.block_height*3/4))
        white_rook_img = pygame.transform.scale(white_rook_img, (self.block_width*1/2, self.block_height*3/4))
        white_knight_img = pygame.transform.scale(white_knight_img, (self.block_width*1/2, self.block_height*3/4))
        white_bishop_img = pygame.transform.scale(white_bishop_img, (self.block_width*1/2, self.block_height*3/4))
        white_queen_img = pygame.transform.scale(white_queen_img, (self.block_width*1/2, self.block_height*3/4))
        white_king_img = pygame.transform.scale(white_king_img, (self.block_width*1/2, self.block_height*3/4))

        #black piece scale
        black_pawn_img = pygame.transform.scale(black_pawn_img, (self.block_width*1/2, self.block_height*3/4))
        black_rook_img = pygame.transform.scale(black_rook_img, (self.block_width*1/2, self.block_height*3/4))
        black_knight_img = pygame.transform.scale(black_knight_img, (self.block_width*1/2, self.block_height*3/4))
        black_bishop_img = pygame.transform.scale(black_bishop_img, (self.block_width*1/2, self.block_height*3/4))
        black_queen_img = pygame.transform.scale(black_queen_img, (self.block_width*1/2, self.block_height*3/4))
        black_king_img = pygame.transform.scale(black_king_img, (self.block_width*1/2, self.block_height*3/4))

        self.b = [black_pawn_img, black_rook_img, black_knight_img, black_bishop_img, black_queen_img, black_king_img]
        self.w = [white_pawn_img, white_rook_img, white_knight_img, white_bishop_img, white_queen_img, white_king_img]

        self.x_pos, self.y_pos = self.block_width*1/4, self.block_height*1/8

        self.has_selected_piece = False
        self.has_selected_block = []
        self.display_board('w')
                                

    def display_board(self, cur_player):
        """_summary_: Blits the boards current information and updates the screen.
        """        
        
        self.window.blit(self.board.img, (0,0))

        blist = []
        
        if cur_player == 'w':
            for piece in self.board.pieces_lst:
                if piece.color == 'b':
                    blist.append((piece.location, self.b[piece.img]))
                else:
                    blist.append((piece.location, self.w[piece.img]))
        
        else:
            for piece in self.board.pieces_lst:
                pos = (7-piece.location[0], 7-piece.location[1])
                if piece.color == 'b':
                    blist.append((pos, self.b[piece.img]))
                else:
                    blist.append((pos, self.w[piece.img]))

        for pair in blist:
            self.window.blit(pair[1], (self.x_pos + pair[0][1]*self.block_width, self.y_pos + pair[0][0]*self.block_height))

        pygame.display.update()


    def is_selected_piece(self, piece):
        """_summary_: Either selects or deselects a piece based on user input

        Args:
            piece (_type_): piece to be selected
        """        
 
        if not self.has_selected_piece == piece:
            self.has_selected_piece = piece
            
        else: self.has_selected_piece = False


    def display_block_border(self):
        """_summary_: Displays a block border surrounding the piece that has been selected and their potential moves
        """             
        
        if self.has_selected_piece:
            p = self.has_selected_piece

            if p.color == 'b':
                #Want to blit highlight of cell to indicate is selected
                pygame.draw.rect(self.window, (255, 0, 0), [7-p.location[1]*self.block_width+1, 7-p.location[0]*self.block_height+1, self.block_height-1, self.block_width-1], 3)

                #blits the cells for all possible moves of self.has_selected_piece
                for move in p.moves:
                    pygame.draw.rect(self.window, (0, 255, 0), [7-move[1]*self.block_width+1, 7-move[0]*self.block_height+1, self.block_height-1, self.block_width-1], 3)
            
            else: 
                #Want to blit highlight of cell to indicate is selected
                pygame.draw.rect(self.window, (255, 0, 0), [p.location[1]*self.block_width+1, p.location[0]*self.block_height+1, self.block_height-1, self.block_width-1], 3)

                #blits the cells for all possible moves of self.has_selected_piece
                for move in p.moves:
                    pygame.draw.rect(self.window, (0, 255, 0), [move[1]*self.block_width+1, move[0]*self.block_height+1, self.block_height-1, self.block_width-1], 3)
        
        pygame.display.update()


    def display_reverse_block(self):
        if self.has_selected_piece:
            p = self.has_selected_piece

            if p.color == 'b':
                #Want to blit highlight of cell to indicate is selected
                pygame.draw.rect(self.window, (255, 0, 0), [(7-p.location[1])*self.block_width, (7-p.location[0])*self.block_height, self.block_height-1, self.block_width-1], 3)

                #blits the cells for all possible moves of self.has_selected_piece
                for move in p.moves:
                    pygame.draw.rect(self.window, (0, 255, 0), [(7-move[1])*self.block_width, (7-move[0])*self.block_height, self.block_height-1, self.block_width-1], 3)
            
            else: 
                #Want to blit highlight of cell to indicate is selected
                pygame.draw.rect(self.window, (255, 0, 0), [p.location[1]*self.block_width+1, 7-p.location[0]*self.block_height+1, self.block_height-1, self.block_width-1], 3)

                #blits the cells for all possible moves of self.has_selected_piece
                for move in p.moves:
                    pygame.draw.rect(self.window, (0, 255, 0), [move[1]*self.block_width+1, 7-move[0]*self.block_height+1, self.block_height-1, self.block_width-1], 3)
        
        pygame.display.update()
    

    def display_in_check(self):
        """_summary_: When move is dissallowed due to being in check, updates the caption of the window to alert 
        player that they are in check
        """        

        pygame.display.set_caption('IN CHECK')
        

    def display_winner(self, winner):
        """_summary_: Displays a png of the winning player at the end of a game

        Args:
            winner (_type_): The team that won the game
        """        

        if winner:
            if self.color == 'b':
                title = pygame.image.load('mvc\\Model\\Imgs\\Black_Wins!.png')
                title = pygame.transform.scale(title, (300, 100))
                self.window.blit(title, (150, 250))
                pygame.display.update()
            
            else:
                title = pygame.image.load('mvc\\Model\\Imgs\\White_Wins!.png')
                title = pygame.transform.scale(title, (300, 100))
                self.window.blit(title, (150, 250))
                pygame.display.update()

        # NEED TO UPDATE WITH LOSER IMAGES     
        else:
            if self.color == 'b':
                title = pygame.image.load('mvc\\Model\\Imgs\\Black_loses.png')
                title = pygame.transform.scale(title, (300, 100))
                self.window.blit(title, (150, 250))
                pygame.display.update()
            
            else:
                title = pygame.image.load('mvc\\Model\\Imgs\\White_loses.png')
                title = pygame.transform.scale(title, (300, 100))
                self.window.blit(title, (150, 250))
                pygame.display.update()