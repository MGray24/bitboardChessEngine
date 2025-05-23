import random

class Engine:
    PIECE_VALUES = {
        'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 0
    }
    def __init__(self, depth=1):
        self.depth = depth
        self.color = "white"

    def choose_move(self, board):
        best_score = -float('inf')
        best_move = None
        for move in board.generate_legal_moves():
            test_board = board.copy()
            test_board.make_move(move)
            score = self.minimax(test_board, self.depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, board, depth, maximizing):
        if depth == 0:
            return self.evaluate(board)

        moves = board.generate_legal_moves()

        if maximizing:
            best = float("-inf")
            for move in moves:
                test_board = board.copy()
                test_board.make_move(move)
                score = self.minimax(test_board, depth - 1, False)
                best = max(best, score)
            return best
        else:
            best = float("inf")
            for move in moves:
                test_board = board.copy()
                test_board.make_move(move)
                score = self.minimax(test_board, depth - 1, True)
                best = min(best, score)
            return best

    def evaluate(self, board): #the color who the engine is playing for
        enemy = "black" if self.color == "white" else "white"
        score = 0
        for piece in board.whitepieces + board.blackpieces:
            for sq in board.get_set_bits(piece.bitboard):
                val = self.PIECE_VALUES[piece.name]
                if piece.color == enemy:
                    val *= -1
                score += val
        return score
