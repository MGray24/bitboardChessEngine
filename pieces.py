from move import Move

def file_a_mask():
    return 0x0101010101010101

def file_h_mask():
    return 0x8080808080808080

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
        self.PAWN_OFFSETS = []

    def generate_moves(self, board):
        moves = []
        occupancy = board.occupancy[self.color]
        enemy = board.occupancy['black' if self.color == 'white' else 'white']
        empty = ~board.occupancy['both']

        bitboard = self.bitboard

        if self.color == 'white':
            # One square forward
            one_push = (bitboard << 8) & empty
            for to_square in board.get_set_bits(one_push):
                from_square = to_square - 8
                if to_square >= 56:
                    # Promotion
                    for promo in ['Q', 'R', 'B', 'N']:
                        moves.append(Move(from_square, to_square, 'P', promotion=promo))
                else:
                    moves.append(Move(from_square, to_square, 'P'))

            # Two square push
            rank2_mask = 0x000000000000FF00
            two_push = ((bitboard & rank2_mask) << 16) & empty & (empty << 8)
            for to_square in board.get_set_bits(two_push):
                from_square = to_square - 16
                moves.append(Move(from_square, to_square, 'P'))

            # Captures
            left_captures = (bitboard << 7) & enemy & ~file_h_mask()
            right_captures = (bitboard << 9) & enemy & ~file_a_mask()

            for to_square in board.get_set_bits(left_captures):
                from_square = to_square - 7
                captured = board.get_piece_at(to_square)
                if to_square >= 56:
                    for promo in ['Q', 'R', 'B', 'N']:
                        moves.append(Move(from_square, to_square, 'P', captured_piece=captured, promotion=promo))
                else:
                    moves.append(Move(from_square, to_square, 'P', captured_piece=captured))

            for to_square in board.get_set_bits(right_captures):
                from_square = to_square - 9
                captured = board.get_piece_at(to_square)
                if to_square >= 56:
                    for promo in ['Q', 'R', 'B', 'N']:
                        moves.append(Move(from_square, to_square, 'P', captured_piece=captured, promotion=promo))
                else:
                    moves.append(Move(from_square, to_square, 'P', captured_piece=captured))

            # En passant
            if board.en_passant_square is not None:
                ep_sq = board.en_passant_square
                if ((bitboard << 7) & (1 << ep_sq)) and (ep_sq % 8 != 7):
                    from_sq = ep_sq - 7
                    moves.append(Move(from_sq, ep_sq, 'P', is_en_passant=True))
                if ((bitboard << 9) & (1 << ep_sq)) and (ep_sq % 8 != 0):
                    from_sq = ep_sq - 9
                    moves.append(Move(from_sq, ep_sq, 'P', is_en_passant=True))

        else: # black pieces
            # One square forward
            one_push = (bitboard >> 8) & empty
            for to_square in board.get_set_bits(one_push):
                from_square = to_square + 8
                if to_square <= 7:
                    # Promotion
                    for promo in ['Q', 'R', 'B', 'N']:
                        moves.append(Move(from_square, to_square, 'P', promotion=promo))
                else:
                    moves.append(Move(from_square, to_square, 'P'))

            # Two square push
            rank7_mask = 0x00FF000000000000
            two_push = ((bitboard & rank7_mask) >> 16) & empty & (empty >> 8)
            for to_square in board.get_set_bits(two_push):
                from_square = to_square + 16
                moves.append(Move(from_square, to_square, 'P'))

            # Captures
            left_captures = (bitboard >> 9) & enemy & ~file_h_mask()
            right_captures = (bitboard >> 7) & enemy & ~file_a_mask()

            for to_square in board.get_set_bits(left_captures):
                from_square = to_square + 9
                captured = board.get_piece_at(to_square)
                if to_square <= 7:
                    for promo in ['Q', 'R', 'B', 'N']:
                        moves.append(Move(from_square, to_square, 'P', captured_piece=captured, promotion=promo))
                else:
                    moves.append(Move(from_square, to_square, 'P', captured_piece=captured))

            for to_square in board.get_set_bits(right_captures):
                from_square = to_square + 7
                captured = board.get_piece_at(to_square)
                if to_square <= 7:
                    for promo in ['Q', 'R', 'B', 'N']:
                        moves.append(Move(from_square, to_square, 'P', captured_piece=captured, promotion=promo))
                else:
                    moves.append(Move(from_square, to_square, 'P', captured_piece=captured))

            # En passant
            if board.en_passant_square is not None:
                ep_sq = board.en_passant_square
                if ((bitboard >> 9) & (1 << ep_sq)) and (ep_sq % 8 != 7):
                    from_sq = ep_sq + 9
                    moves.append(Move(from_sq, ep_sq, 'P', is_en_passant=True))
                if ((bitboard >> 7) & (1 << ep_sq)) and (ep_sq % 8 != 0):
                    from_sq = ep_sq + 7
                    moves.append(Move(from_sq, ep_sq, 'P', is_en_passant=True))
        return moves

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
        moves = []
        occupancy = board.occupancy[self.color]
        enemy = board.occupancy['black' if self.color == 'white' else 'white']
        all_occ = board.occupancy['both']

        for from_square in board.get_set_bits(self.bitboard):
            for direction in [9, -7, -9, 7]:
                to_square = from_square
                while True:
                    to_square += direction

                    # Stop if out of bounds
                    if to_square < 0 or to_square >= 64:
                        break

                    # Prevent wrapping around the board diagonally
                    file_diff = abs((from_square % 8) - (to_square % 8))
                    rank_diff = abs((from_square // 8) - (to_square // 8))
                    if file_diff != rank_diff:
                        break

                    if (occupancy >> to_square) & 1:
                        break  # friendly piece blocking

                    captured = None
                    if (enemy >> to_square) & 1:
                        captured = board.get_piece_at(to_square)
                        moves.append(Move(from_square, to_square, piece_type='B', captured_piece=captured))
                        break  # enemy piece captured; stop ray

                    moves.append(Move(from_square, to_square, piece_type='B'))
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'R', 0x0000000000000081, 0x8100000000000000)

    def generate_moves(self, board):
        moves = []
        occupancy = board.occupancy[self.color]
        enemy = board.occupancy['black' if self.color == 'white' else 'white']
        all_occ = board.occupancy['both']

        for from_square in board.get_set_bits(self.bitboard):
            for direction in [8, -8, 1, -1]:  # up, down, right, left
                to_square = from_square
                while True:
                    # Step one square in that direction
                    to_square += direction

                    # Board bounds check
                    if to_square < 0 or to_square >= 64:
                        break
                    if direction == 1 and to_square % 8 == 0:  # wrapped from h to a
                        break
                    if direction == -1 and to_square % 8 == 7:  # wrapped from a to h
                        break

                    if (occupancy >> to_square) & 1:
                        break  # Blocked by own piece

                    captured = None
                    if (enemy >> to_square) & 1:
                        captured = board.get_piece_at(to_square)
                        moves.append(Move(from_square, to_square, piece_type='R', captured_piece=captured))
                        break  # Can capture but can't go further
                    else:
                        moves.append(Move(from_square, to_square, piece_type='R'))
        return moves

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Q', 0x0000000000000008, 0x0800000000000000)

    def generate_moves(self, board):
        moves = []
        occupancy = board.occupancy[self.color]
        enemy = board.occupancy['black' if self.color == 'white' else 'white']
        all_occ = board.occupancy['both']

        for from_square in board.get_set_bits(self.bitboard):
            for direction in [8, -8, 1, -1, 9, -7, -9, 7]:
                to_square = from_square
                while True:
                    to_square += direction

                    # Stop if out of bounds
                    if to_square < 0 or to_square >= 64:
                        break

                    # Prevent horizontal or diagonal wrap
                    file_diff = abs((from_square % 8) - (to_square % 8))
                    rank_diff = abs((from_square // 8) - (to_square // 8))
                    if direction == 1 and to_square % 8 == 0:  # wrapped from h to a
                        break
                    if direction == -1 and to_square % 8 == 7:  # wrapped from a to h
                        break
                    if direction in [9, -7, -9, 7] and file_diff != rank_diff:
                        break  # diagonal wrap

                    if (occupancy >> to_square) & 1:
                        break  # own piece blocks

                    captured = None
                    if (enemy >> to_square) & 1:
                        captured = board.get_piece_at(to_square)
                        moves.append(Move(from_square, to_square, piece_type='Q', captured_piece=captured))
                        break  # capture, then stop

                    moves.append(Move(from_square, to_square, piece_type='Q'))
        return moves

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K', 0x0000000000000010, 0x1000000000000000)

    def generate_moves(self, board):
        moves = []
        occupancy = board.occupancy[self.color]
        enemy = board.occupancy['black' if self.color == 'white' else 'white']

        for from_square in board.get_set_bits(self.bitboard):
            for direction in [8, -8, 1, -1, 9, -7, -9, 7]:
                to_square = from_square + direction

                # Check bounds
                if to_square < 0 or to_square >= 64:
                    continue

                # Prevent wrapping (like from h1 → a2)
                file_diff = abs((from_square % 8) - (to_square % 8))
                rank_diff = abs((from_square // 8) - (to_square // 8))
                if file_diff > 1 or rank_diff > 1:
                    continue

                if (occupancy >> to_square) & 1:
                    continue  # can't move onto own piece

                captured = None
                if (enemy >> to_square) & 1:
                    captured = board.get_piece_at(to_square)

                moves.append(Move(from_square, to_square, piece_type='K', captured_piece=captured))

        return moves
