from move import Move

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

    def generate_moves(self, board):
        return []

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'N', 0x0000000000000042, 0x4200000000000000)

        self.KNIGHT_OFFSETS = [17, 15, 10, 6, -17, -15, -10, -6]

    def generate_moves(self, board):
        moves = []
        occupancy = board.occupancy[self.color]
        enemy = board.occupancy['black' if self.color == 'white' else 'white']

        for from_square in board.get_set_bits(self.bitboard):
            for offset in self.KNIGHT_OFFSETS:
                to_square = from_square + offset
                if 0 <= to_square < 64 and self.is_knight_jump_valid(from_square, to_square):
                    if not (occupancy >> to_square) & 1:
                        captured_piece = None
                        if (enemy >> to_square) & 1:
                            captured_piece = board.get_piece_at(to_square)
                        moves.append(Move(from_square, to_square, piece_type='N', captured_piece=captured_piece))
        return moves

    def is_knight_jump_valid(self, from_sq, to_sq):
        # Prevent wraparound (e.g. h1 to a2)
        file_diff = abs((from_sq % 8) - (to_sq % 8))
        rank_diff = abs((from_sq // 8) - (to_sq // 8))
        return sorted((file_diff, rank_diff)) == [1, 2]


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'B', 0x0000000000000024, 0x2400000000000000)

    def generate_moves(self, board):
        return []

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'R', 0x0000000000000081, 0x8100000000000000)

    def generate_moves(self, board):
        return []

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Q', 0x0000000000000008, 0x0800000000000000)

    def generate_moves(self, board):
        return []

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K', 0x0000000000000010, 0x1000000000000000)

    def generate_moves(self, board):
        return []
