#for bitboards, the first bit represents a1 (bottom left), it increases by going to the right, then up
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
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
        
        self.white_pos = 0
        self.black_pos = 0
        self.both_pos = 0
        self.setColorBoards()
        self.side_to_move = 'white'
        self.castling_rights = 0b1111  # WK, WQ, BK, BQ
        self.en_passant_square = None # stores a square where en passant is possible 0-63
        self.halfmove_clock = 0 # for 50 move rule
        self.fullmove_number = 0 # number of full moves for stats


    def setColorBoards(self):
        self.white_pos = 0
        for piece in self.whitepieces:
            self.white_pos = self.white_pos | piece.bitboard

        self.black_pos = 0
        for piece in self.blackpieces:
            self.black_pos = self.black_pos | piece.bitboard

        self.both_pos = self.white_pos | self.black_pos

    