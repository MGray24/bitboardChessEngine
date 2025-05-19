from board import Board
from move import Move

class Game:
    def __init__(self):
        self.board = Board()
        self.selected_square = None
        self.legal_moves = self.board.generate_legal_moves()
        self.highlights = {}
        self.last_move = None

    def handle_click(self, square):
        if self.selected_square is None:
            # First click: select piece
            piece = self.board.get_piece_at(square)
            if piece and piece.color == self.board.side_to_move:
                self.selected_square = square
                self.legal_moves = self.board.generate_legal_moves() #generate moves from this square
        else:
            # Second click: attempt move
            for move in self.legal_moves:
                if move.from_square == self.selected_square and move.to_square == square:
                    self.board.make_move(move)
                    self.last_move = move
                    break

            self.selected_square = None  # Reset either way
    def get_highlight_squares(self):
        highlights = {}

        if self.last_move:
            highlights[self.last_move.from_square] = (255, 215, 0)  # gold
            highlights[self.last_move.to_square] = (255, 215, 0)

        if self.selected_square is not None:
            highlights[self.selected_square] = (100, 149, 237)  # blue

            # Highlight all possible destinations
            for move in self.legal_moves:
                if move.from_square == self.selected_square:
                    highlights[move.to_square] = (144, 238, 144)  # light green

        return highlights
