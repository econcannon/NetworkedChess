#Move this file into Model file to use
from board import Board
from game import Game

board = Board(600, 600)
g = Game(board)#
#rook = Rook('b', (3,1))
#print(rook)
#print(rook.color)

print(board)

a = board.get_cell(0, 1)
a.append_moves(board)

g.execute_move(board.board[0][1], a.moves[0])

print('\n', board)

a = board.get_cell(0,0)
a.append_moves(board)

g.execute_move(board.board[0][0], a.moves[0])

print('\n', board)

