from mvc.Model.pieces import Pieces 

class Bishop(Pieces):

    def __init__(self, color, location) -> None:
        super().__init__(color, location)
        self.img = 3
        self.turn = 0


    def append_moves(self, board):
        """_summary_: Appends moves to piece's move_list attribute based on current board conditions and piece's
        allowed movement

        Args:
            board (_type_): the current board object
        """        
        i = 0
        self.moves = []
        subset = []

        #move to top right
        for i in range(1,8):

            x = self.location[0] + i, self.location[1] + i
            if (x[0] > 7) or (x[1] > 7) or (x[0] < 0) or (x[1] < 0):
                break

            if board.get_cell(x[0], x[1]) != 0:
                if board.get_cell(x[0], x[1]).color != self.color:
                    self.moves.append(x)
                    break
                else: break
            
            else: self.moves.append(x)
        
        #Move to top left
        for i in range(1,8):

            x = self.location[0] + i, self.location[1] - i
            if (x[0] > 7) or (x[1] > 7) or (x[0] < 0) or (x[1] < 0):
                break

            if board.get_cell(x[0], x[1]) != 0:
                if board.get_cell(x[0], x[1]).color != self.color:
                    self.moves.append(x)
                    break
                else: break
            
            else: self.moves.append(x)

        #Move to bottom left
        for i in range(1,8):

            x = self.location[0] - i, self.location[1] - i
            if (x[0] > 7) or (x[1] > 7) or (x[0] < 0) or (x[1] < 0):
                break

            if board.get_cell(x[0], x[1]) != 0:
                if board.get_cell(x[0], x[1]).color != self.color:
                    self.moves.append(x)
                    break
                else: break
            
            else: self.moves.append(x)

        
        #Move to bottom right
        for i in range(1,8):

            x = self.location[0] - i, self.location[1] + i
            if (x[0] > 7) or (x[1] > 7) or (x[0] < 0) or (x[1] < 0):
                break

            if board.get_cell(x[0], x[1]) != 0:
                if board.get_cell(x[0], x[1]).color != self.color:
                    self.moves.append(x)
                    break
                else: break
            
            else: self.moves.append(x)


    def move_piece(self):
        pass


    def __str__(self):
        return f'Bishop'