import pygame
from board import Board
from game import Game
from renderer import Renderer

def main():
    pygame.init()
    screen = pygame.display.set_mode((920, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Bitboard Chess")
    game = Game()
    renderer = Renderer(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                renderer.set_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos # Gets the mouse coordinates
                # Adjust for the board's starting position
                adjusted_x = x - renderer.DRAW_START[0]
                adjusted_y = y - renderer.DRAW_START[1]
                column = adjusted_x // renderer.SQUARE_SIZE
                row = 7 - adjusted_y // renderer.SQUARE_SIZE 
                square_number = int(row * 8 + column)
                print(f"Row: {row}, Column: {column}, {square_number}")
                game.handle_click(square_number)
        renderer.draw_board(game.get_highlight_squares())
        renderer.draw_pieces(game.board)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

