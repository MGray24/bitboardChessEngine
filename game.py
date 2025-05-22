from board import Board
from move import Move
from renderer import Renderer
from engine import Engine

'''
if state == 'checkmate':
    print("Checkmate!")
elif state == 'check':
    print("Check!")
elif state == 'stalemate':
    print("Stalemate!")
else:
    print("Normal")
break'''

class Game:
    def __init__(self):
        self.board = Board()
        self.selected_square = None
        self.legal_moves = self.board.generate_legal_moves()
        self.highlights = {}
        self.last_move = None
        self.engine = Engine()

    def make_engine_move(self):
        move = self.engine.choose_move(self.board)
        if move:
            self.board.make_move(move)
            self.legal_moves = self.board.generate_legal_moves()
            self.last_move = move

    def handle_click(self, x, y, renderer):
        if renderer.board_rect.collidepoint(x, y):
            # Adjust for the board's starting position
            adjusted_x = x - renderer.DRAW_START[0]
            adjusted_y = y - renderer.DRAW_START[1]
            column = adjusted_x // renderer.SQUARE_SIZE
            row = 7 - adjusted_y // renderer.SQUARE_SIZE
            square = int(row * 8 + column)
            # print(f"Row: {row}, Column: {column}, {square_number}")
            if self.selected_square is None:
                # First click: select piece
                piece = self.board.get_piece_at(square)
                if piece and piece.color == self.board.side_to_move:
                    self.selected_square = square
                    self.legal_moves = self.board.generate_legal_moves() #generate moves from this square
            else:
                # Second click: attempt move
                # Get all matching from → to moves
                candidates = [
                    move for move in self.legal_moves
                    if move.from_square == self.selected_square and move.to_square == square
                ]

                if not candidates:
                    self.selected_square = None
                    return

                # If none of the matching moves are promotions, there's only one valid option
                non_promos = [m for m in candidates if m.promotion is None]
                if len(non_promos) == 1:
                    self.board.make_move(non_promos[0])
                    self.legal_moves = self.board.generate_legal_moves()
                    self.last_move = non_promos[0]
                    self.selected_square = None
                    return

                # Otherwise, this is a promotion — ask the player what piece they want
                promoted_piece = self.prompt_for_promotion()

                # Find the matching promotion move
                for move in candidates:
                    if move.promotion == promoted_piece:
                        self.board.make_move(move)
                        self.legal_moves = self.board.generate_legal_moves()
                        self.last_move = move
                        break

                self.selected_square = None  # Reset either way

    def get_highlight_squares(self):
        highlights = {}

        if self.last_move:
            highlights[self.last_move.from_square] = (255, 215, 0)  # gold
            highlights[self.last_move.to_square] = (255, 215, 0)

        if self.selected_square is not None:
            highlights[self.selected_square] = (100, 149, 237)  # blue

            # Highlight all possible destinations
            for move in self.legal_moves:
                if move.from_square == self.selected_square:
                    highlights[move.to_square] = (144, 238, 144)  # light green

        return highlights

    def get_game_state(self):
        legal_moves = self.board.generate_legal_moves()
        in_check = self.board.is_in_check(self.board.side_to_move)

        if in_check and not legal_moves:
            return 'checkmate'
        elif not in_check and not legal_moves:
            return 'stalemate'
        elif in_check:
            return 'check'
        else:
            return 'normal'

    def prompt_for_promotion(self):
        # TEMP: always promote to queen
        return 'Q'