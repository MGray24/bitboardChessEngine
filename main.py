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
                x, y = event.pos
                game.handle_click(x, y, renderer)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.make_engine_move()
        renderer.draw_board(game.get_highlight_squares())
        renderer.draw_pieces(game.board)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

