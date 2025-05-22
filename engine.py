import random

class Engine:
    def __init__(self, depth=1):
        self.depth = depth

    def choose_move(self, board):
        legal_moves = board.generate_legal_moves()
        if not legal_moves:
            return None

        # For now, just pick a random legal move
        return random.choice(legal_moves)
