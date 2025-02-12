import pygame
from generate_board import generate_sudoku

pygame.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Sudoku")

full_board, game_board = generate_sudoku(num_remove=40)

def main():
    running = True
    clock = pygame.time.Clock()  # Přidání časovače pro kontrolu FPS

    while running:
        screen.fill((255, 255, 255))  # Vyplní obrazovku bílou barvou

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  # Aktualizuje obrazovku
        clock.tick(30)  # Omezí smyčku na 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()