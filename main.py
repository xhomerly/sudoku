import pygame
from generate_board import generate_sudoku

pygame.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Sudoku")

full_board, game_board = generate_sudoku(num_remove=40)

GRID_SIZE = 450
CELL_SIZE = GRID_SIZE // 9
OFFSET_X = 25
OFFSET_Y = 75
font = pygame.font.SysFont(None, 50)

selected_cell = None
player_board = [list(row) for row in game_board] # Kopie herní desky pro hráče
incorrect_cells = set()

def draw_grid():
    for row in range(10):
        if row % 3 == 0:
            thickness = 4  # Tlustší čára po každých 3 řádcích
        else:
            thickness = 1
        pygame.draw.line(screen, (0, 0, 0),
                         (OFFSET_X, OFFSET_Y + row * CELL_SIZE),
                         (OFFSET_X + GRID_SIZE, OFFSET_Y + row * CELL_SIZE),
                         thickness)
        pygame.draw.line(screen, (0, 0, 0),
                         (OFFSET_X + row * CELL_SIZE, OFFSET_Y),
                         (OFFSET_X + row * CELL_SIZE, OFFSET_Y + GRID_SIZE),
                         thickness)

def draw_numbers():
    for row in range(9):
        for col in range(9):
            num = player_board[row][col]  # Use player_board instead of game_board
            if num != 0:
                text = font.render(str(num), True, (0, 0, 0))
                x = OFFSET_X + col * CELL_SIZE + CELL_SIZE // 3
                y = OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 5
                screen.blit(text, (x, y))


def draw_selection():
    for row, col in incorrect_cells:
        pygame.draw.rect(screen, (255, 150, 150),
                         (OFFSET_X + col * CELL_SIZE, OFFSET_Y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if selected_cell:
        pygame.draw.rect(screen, (0, 0, 255),
                         (OFFSET_X + selected_cell[1] * CELL_SIZE, OFFSET_Y + selected_cell[0] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE), 3)

def handle_key(key):
    if selected_cell and (pygame.K_1 <= key <= pygame.K_9 or pygame.K_KP1 <= key <= pygame.K_KP9):
        row, col = selected_cell
        if pygame.K_1 <= key <= pygame.K_9:  # Regular number keys
            value = key - pygame.K_1 + 1
        elif pygame.K_KP1 <= key <= pygame.K_KP9:  # Keypad number keys
            value = key - pygame.K_KP1 + 1
        player_board[row][col] = value
        if full_board[row][col] != value:
            incorrect_cells.add((row, col))
        else:
            incorrect_cells.discard((row, col))

def handle_click(pos):
    x, y = pos
    if OFFSET_X < x < OFFSET_X + GRID_SIZE and OFFSET_Y < y < OFFSET_Y + GRID_SIZE:
        col = (x - OFFSET_X) // CELL_SIZE
        row = (y - OFFSET_Y) // CELL_SIZE
        return row, col
    return None

def main():
    global selected_cell
    running = True
    clock = pygame.time.Clock()  # Přidání časovače pro kontrolu FPS

    while running:
        screen.fill((255, 255, 255))
        draw_grid()
        draw_selection()
        draw_numbers()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_cell = handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                handle_key(event.key)
                if event.key == pygame.K_ESCAPE:
                    selected_cell = None

        pygame.display.flip()  # Aktualizuje obrazovku
        clock.tick(30)  # Omezí smyčku na 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()