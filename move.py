class Move:
    def __init__(self, from_square, to_square, piece_type=None, captured_piece=None, promotion=None, is_castle=False, is_en_passant=False):
        self.from_square = from_square  # int 0–63
        self.to_square = to_square      # int 0–63
        self.piece_type = piece_type    # e.g. 'P', 'N'
        self.captured_piece = captured_piece  # e.g. 'p' or None
        self.promotion = promotion      # e.g. 'Q' or None
        self.is_castle = is_castle
        self.is_en_passant = is_en_passant

    def __eq__(self, other):
        return (self.from_square == other.from_square and
                self.to_square == other.to_square and
                self.promotion == other.promotion)

    def __hash__(self):
        return hash((self.from_square, self.to_square, self.promotion))

    def __repr__(self):
        return f"Move({self.from_square} -> {self.to_square}, promotion={self.promotion})"
