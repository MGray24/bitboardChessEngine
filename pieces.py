class Piece:
    def __init__(self, color, name, initial_bitboard_white, initial_bitboard_black):
        if color not in ("white", "black"):
            raise ValueError("Color must be 'white' or 'black'")
        self.color = color
        self.name = name  # 'P', 'N', etc.
        self.bitboard = (
            initial_bitboard_white if color == "white" else initial_bitboard_black
        )

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'P', 0x000000000000FF00, 0x00FF000000000000)

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'N', 0x0000000000000042, 0x4200000000000000)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'B', 0x0000000000000024, 0x2400000000000000)

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'R', 0x0000000000000081, 0x8100000000000000)

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Q', 0x0000000000000008, 0x0800000000000000)

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K', 0x0000000000000010, 0x1000000000000000)
