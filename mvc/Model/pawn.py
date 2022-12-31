from mvc.Model.pieces import Pieces

class Pawn(Pieces):

    def __init__(self, color, location) -> None:
        super().__init__(color, location)
        self.img = 0
        self.turn = 0

    
    def append_moves(self, board):
        """_summary_: Appends moves to piece's move_list attribute based on current board conditions and piece's
        allowed movement

        Args:
            board (_type_): the current board object
        """        
        self.moves = []
        x = []

        if self.color == 'b':

            if (self.location[0] + 1 < 8):

                if board.get_cell(self.location[0] + 1, self.location[1]) == 0:
                    x.append((self.location[0] + 1, self.location[1]))

            if self.turn == 0:
                if (board.get_cell(self.location[0]+1, self.location[1]) == 0) and (board.get_cell(self.location[0]+2, self.location[1])) == 0:
                    x.append((self.location[0] + 2, self.location[1]))

            #test diagonal
            if (self.location[0] + 1 < 8) and (self.location[1] + 1 < 8):
                cell = board.get_cell(self.location[0] + 1, self.location[1] + 1)
                if cell != 0:
                    if cell.color != self.color:
                        x.append((self.location[0] + 1, self.location[1] + 1))

            #test other diagonal
            if (self.location[0] + 1 < 8) and (self.location[1] - 1 > -1):
                cell = board.get_cell(self.location[0] + 1, self.location[1] - 1)
                if cell != 0:
                    if cell.color != self.color:
                        x.append((self.location[0] + 1, self.location[1] - 1))
            
        if self.color == 'w':

            if (self.location[0] - 1 > 0):
                if board.get_cell(self.location[0] - 1, self.location[1]) == 0:
                    x.append((self.location[0] - 1, self.location[1]))

            if self.turn == 0:
                if (board.get_cell(self.location[0] - 1, self.location[1]) == 0) and (board.get_cell(self.location[0] - 2, self.location[1])) == 0:
                    x.append((self.location[0] - 2, self.location[1]))

            #test diagonal 
            if (self.location[0] - 1 > -1) and (self.location[1] + 1 < 8):
                cell = board.get_cell(self.location[0] - 1, self.location[1] + 1)
                if cell != 0:
                    if cell.color != self.color:
                        x.append((self.location[0] - 1, self.location[1] + 1))

            #test other diagonal
            if (self.location[0] - 1 > -1) and (self.location[1] - 1 > -1):
                cell = board.get_cell(self.location[0] - 1, self.location[1] - 1)
                if cell != 0:
                    if cell.color != self.color:
                        x.append((self.location[0] - 1, self.location[1] - 1))
        
        for pos in x:
            if (pos[0] < 0) or (pos[0] > 7) or (pos[1] < 0) or (pos[1] > 7):
                x.remove(pos)
                continue
            else: self.moves.append(pos)


    def __str__(self) -> str:
        return f'Pawn'