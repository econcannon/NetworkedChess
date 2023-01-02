from chess_server1 import Chess_Server
from chess_client1 import Chess_Client

# Determine host or client side
while True:
    print('Do you want to host this game?\n')
    response = input('Enter \'y\' or \'n\'')

    if (response == 'y') or (response == 'n'):
        break
    else: print('Invalid Input, please try again...')

# Initialize respective connection end
if response == 'y':
    server = Chess_Server()

else: 
    client = Chess_Client()

# Game over, close sockets
if response == 'y':
    server.disconnect()
else: client.disconnect()