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

    def get_set_bits(self, bitboard): # returns numbers 0-63, representing bits that are set
        while bitboard:
            lsb = bitboard & -bitboard
            square = lsb.bit_length() - 1
            yield square
            bitboard &= bitboard - 1

    def generate_legal_moves(self):
        moves = []
        active_pieces = self.whitepieces if self.side_to_move == 'white' else self.blackpieces
        for piece in active_pieces:
            moves.extend(piece.generate_moves(self))
        return moves

    def make_move(self, move):
        #set en passant square
        if move.piece_type == 'P' and abs(move.from_square - move.to_square) == 16:
            # Pawn double move
            direction = -8 if self.side_to_move == 'white' else 8
            self.en_passant_square = move.to_square + direction
        else:
            self.en_passant_square = None

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


