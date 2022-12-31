from mvc.View.game_view import GameView
from mvc.Model.board import Board
from mvc.Model.game import Game

board = Board()
game = Game()

gv = GameView(board, game)
gv.display_board()