from board import Board
from move import Move

class Game:
    def __init__(self):
        self.board = Board()
        self.selected_square = None
        #self.legal_moves = self.board.generate_legal_moves()

    def handle_click(self, square):
        if self.selected_square is None:
            # First click: select piece
            piece = self.board.get_piece_at(square)
            if piece and piece.color == self.board.side_to_move:
                self.selected_square = square
        else:
            # Second click: attempt move
            move = Move(self.selected_square, square)
            '''
            if move in self.legal_moves:
                self.board.make_move(move)
                self.legal_moves = self.board.generate_legal_moves()
            '''
            self.board.make_move(move)
            self.selected_square = None  # Reset either way
    def get_highlighted_squares(self):
        '''
        if self.selected_square is None:
            return []
        return [m.to_square for m in self.legal_moves if m.from_square == self.selected_square]
        '''
