import pygame
from board import Board
from renderer import Renderer

def main():
    pygame.init()
    screen = pygame.display.set_mode((920, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Bitboard Chess")
    board = Board()
    renderer = Renderer(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                renderer.set_screen()
        renderer.draw_board()
        renderer.draw_pieces(board)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


