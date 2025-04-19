class Board:
    def __init__(self):
        self.bitboards = { #bitboards for every type of piece
            'wP': 0, 'wN': 0, 'wB': 0, 'wR': 0, 'wQ': 0, 'wK': 0,
            'bP': 0, 'bN': 0, 'bB': 0, 'bR': 0, 'bQ': 0, 'bK': 0,
        }
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

    def init_position(self):
        #set starting bitboards, Bottom left is index 0, top right is 63
        self.bitboards['wP'] = 0x000000000000FF00
        self.bitboards['wR'] = 0x0000000000000081
        self.bitboards['wN'] = 0x0000000000000042
        self.bitboards['wB'] = 0x0000000000000024
        self.bitboards['wQ'] = 0x0000000000000008
        self.bitboards['wK'] = 0x0000000000000010

        self.bitboards['bP'] = 0x00FF000000000000
        self.bitboards['bR'] = 0x8100000000000000
        self.bitboards['bN'] = 0x4200000000000000
        self.bitboards['bB'] = 0x2400000000000000
        self.bitboards['bQ'] = 0x0800000000000000
        self.bitboards['bK'] = 0x1000000000000000

        self.update_occupancy()

    def update_occupancy(self):
        pass
