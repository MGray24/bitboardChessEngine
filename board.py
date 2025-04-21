#for bitboards, the first bit represents a1 (bottom left), it increases by going to the right, then up
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
class Board:
    def __init__(self):
        self.whitebitboards = [
            Pawn('white'),           
            Knight('white'), 
            Bishop('white'), 
            Rook('white'), 
            Queen('white'), 
            King('white')]
        
        
        '''
        self.occupancy = { #bitboards for more general pieces
            'white': 0,
            'black': 0,
            'both': 0
        }
        self.side_to_move = 'white'
        self.castling_rights = 0b1111  # WK, WQ, BK, BQ
        self.en_passant_square = None # stores a square where en passant is possible 0-63
        self.halfmove_clock = 0 # for 50 move rule
        self.fullmove_number = 0 # number of full moves for stats
        self.init_position()
        '''

    def init_position(self):
        #set starting bitboards, Bottom left is index 0, top right is 63
        pass

    def update_occupancy(self):
        pass

class SetColorBoards:

    def newboard(self):
        all_white = 0
        for piece in self.whitebitboards:
            all_white = all_white | piece.bitboard