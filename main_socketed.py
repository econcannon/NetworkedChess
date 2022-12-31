from mvc.Controller.game_controller import GameController
from chess_server import Chess_Server
from chess_client import Chess_Client

import pygame

# Determine host or client side
while True:
    print('Do you want to host this game?')
    response = input('Enter \'y\' or \'n\'')

    if (response == 'y') or (response == 'n'):
        break
    else: print('Invalid Input, please try again...')

# Initialize pygame 
pygame.init()

# Initialize respective connection end
if response == 'y':
    server = Chess_Server()
    color = server.color

    # Initialize the GameController and start the game
    gcont = GameController(color, server)
    gcont.start_game()  

else: 
    client = Chess_Client()
    color = client.color

    # Initialize the GameController and start the game
    gcont = GameController(color, client)
    gcont.start_game()



