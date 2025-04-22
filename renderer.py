import pygame
import os

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.screen = pygame.display.set_mode((self.screen.get_width(),int((66/91) * self.screen.get_width())))
        self.width, self.height = self.screen.get_size()
        self.DRAW_START = (self.height/66 + 1, self.height/66 + 1)  # where to put top left corner of board
        self.SQUARE_SIZE = int(self.height * (8/66))
        self.BOARD_SIZE = self.SQUARE_SIZE * 8
        self.LIGHT_COLOR = (240, 217, 181)
        self.DARK_COLOR = (181, 136, 99)
        self.FONT_COLOR = (0, 0, 0)

        self.font = pygame.font.SysFont("arial", 48)
        self.images = self.load_piece_images("assets")

    def load_piece_images(self, folder_path):
        images = {}
        for color in ('w', 'b'):
            for piece in ('p', 'n', 'b', 'r', 'q', 'k'):
                key = color + piece
                subfolder = "white" if color == 'w' else "black"
                path = os.path.join(folder_path, subfolder, f"{key}.png")
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (self.SQUARE_SIZE, self.SQUARE_SIZE))
                key = color + piece.upper()
                images[key] = image
        return images

    def draw_board(self):
        self.screen.fill("gray30")
        for rank in range(8):
            for file in range(8):
                color = self.LIGHT_COLOR if (rank + file) % 2 == 0 else self.DARK_COLOR
                rect = pygame.Rect(file * self.SQUARE_SIZE + self.DRAW_START[0], (7 - rank) * self.SQUARE_SIZE + self.DRAW_START[1], self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def draw_pieces(self, board):
        pass

    def get_set_bits(self, bitboard): # returns numbers 0-63, representing bits that are set
        while bitboard:
            lsb = bitboard & -bitboard
            square = lsb.bit_length() - 1
            yield square
            bitboard &= bitboard - 1
