import pygame
from pygame.locals import *

class Game:

    def __init__(self) -> None:
        
        self.img = pygame.image.load('mvc\\Model\\Imgs\\board.png')
        self.img_blit = pygame.image.load('mvc\\Model\\Imgs\\white_pawn.png')
        self.img = pygame.transform.scale(self.img, (500, 500))
        self.window = pygame.display.set_mode((600, 600))
        self.check = True
        self.pos = [0, 0]
    
    def display_img(self, img = 0):
        self.window.blit(self.img, (10,10))
        run = True
        count = 0
        while run:
            count += 1
            self.window.blit(self.img_blit, (10, 10))
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if self.check:
                        self.prove_input()
                    else:
                        self.further_proof()

                if event.type == pygame.QUIT:
                    run = False
            
            pygame.display.update()

    
    def prove_input(self):
        self.window.blit(self.img_blit, (self.pos[0], self.pos[1]))
        self.check = False
    
    def further_proof(self):
        self.pos[0] += 5
        self.pos[1] += 5