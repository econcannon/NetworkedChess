from mvc.Model.pieces import Pieces

class King(Pieces):

    def __init__(self, color, location) -> None:
        super().__init__(color, location)
        self.img = 5
        self.turn = 0
    

    def append_moves(self, board):
        """_summary_: Appends moves to piece's move_list attribute based on current board conditions and piece's
        allowed movement

        Args:
            board (_type_): the current board object
        """        
        self.moves = []
        x = []
        x.append((self.location[0] - 1, self.location[1]))    
        x.append((self.location[0] + 1, self.location[1]))                    
        x.append((self.location[0] + 1, self.location[1] + 1))            
        x.append((self.location[0] + 1, self.location[1] - 1))                   
        x.append((self.location[0], self.location[1] + 1))       
        x.append((self.location[0], self.location[1] - 1))
        x.append((self.location[0] - 1, self.location[1] + 1))
        x.append((self.location[0] - 1, self.location[1] - 1))

        inv_moves = []

        for pos in x:
            if (pos[0] > 7) or (pos[1] > 7) or (pos[0] < 0) or (pos[1] < 0):
                inv_moves.append(pos)
                continue

            cell = board.get_cell(pos[0], pos[1])
            if cell != 0:
                if cell.color == self.color:
                    inv_moves.append(pos)
                    continue

        for move in inv_moves:
            if move in x:
                x.remove(move)

        for move in x:
            self.moves.append(move)


    def __str__(self) -> str:
        return f'King'