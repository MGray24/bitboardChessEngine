#for bitboards, the first bit represents a1 (bottom left), it increases by going to the right, then up
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from move import Move
class Board:
    def __init__(self):
        self.whitepieces = [
            Pawn('white'),           
            Knight('white'), 
            Bishop('white'), 
            Rook('white'), 
            Queen('white'), 
            King('white')
        ]

        self.blackpieces = [
            Pawn('black'),
            Knight('black'),
            Bishop('black'),
            Rook('black'),
            Queen('black'),
            King('black')
        ]
        self.occupancy = {
            "white": 0,  # all squares occupied by white pieces
            "black": 0,  # all squares occupied by black pieces
            "both": 0,  # all squares with any piece
        }
        self.white_pos = 0
        self.black_pos = 0
        self.both_pos = 0
        self.set_color_boards()
        self.side_to_move = 'white'
        self.castling_rights = 0b1111  # WK, WQ, BK, BQ
        self.en_passant_square = None # stores a square where en passant is possible 0-63
        self.halfmove_clock = 0 # for 50 move rule
        self.fullmove_number = 0 # number of full moves for stats
        move = Move(0, 11)
        self.make_move(move)

    def set_color_boards(self):
        self.occupancy["white"] = 0
        for piece in self.whitepieces:
            self.occupancy["white"] = self.white_pos | piece.bitboard

        self.occupancy["black"] = 0
        for piece in self.blackpieces:
            self.occupancy["black"] = self.black_pos | piece.bitboard

        self.occupancy["both"] = self.occupancy["white"] | self.occupancy["black"]

    def get_piece_at(self, square):
        all_pieces = self.whitepieces + self.blackpieces
        for piece in all_pieces:
            if (piece.bitboard >> square) & 1:
                return piece
        return None

    def make_move(self, move):
        # 1. Identify the moving piece
        piece = self.get_piece_at(move.from_square)
        if not piece:
            raise ValueError("No piece at from_square")

        # 2. Remove piece from the original square
        piece.bitboard &= ~(1 << move.from_square)

        # 3. Handle captures
        captured = self.get_piece_at(move.to_square)
        if captured:
            captured.bitboard &= ~(1 << move.to_square)

        # 4. Place the piece on the new square
        piece.bitboard |= (1 << move.to_square)

        # 5. Handle promotions
        '''
        if move.promotion:
            piece.bitboard &= ~(1 << move.to_square)  # remove pawn
            promoted_piece = self.get_promoted_piece(move.promotion, piece.color)
            promoted_piece.bitboard |= (1 << move.to_square)
        '''

        # 6. Update game state
        self.side_to_move = 'black' if self.side_to_move == 'white' else 'white'
        self.set_color_boards()


