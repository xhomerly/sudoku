import pygame
import time
from generate_board import generate_sudoku

pygame.init()
screen = pygame.display.set_mode((500, 640))
pygame.display.set_caption("Sudoku")

full_board, game_board = generate_sudoku(num_remove=40)

GRID_SIZE = 450
CELL_SIZE = GRID_SIZE // 9
OFFSET_X = 25
OFFSET_Y = 75
NUMBER_BAR_Y = OFFSET_Y + GRID_SIZE + 10
font = pygame.font.SysFont(None, 50)
timer_font = pygame.font.SysFont(None, 35)
desc_font = pygame.font.SysFont(None, 30)

selected_cell = None
player_board = [list(row) for row in game_board]  # Copy of game board for player
incorrect_cells = set()
mistakes = 0
max_mistakes = 3
start_time = time.time()
game_over = False
hidden_numbers = set()


def print_board(board):  # For testing purposes only
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("-" * 21)  # Horizontal separator every 3 rows
        for col in range(9):
            if col % 3 == 0 and col != 0:
                print("| ", end="")  # Vertical separator every 3 columns
            print(f"{board[row][col] if board[row][col] != 0 else '.'} ", end="")
        print()  # New line after each row


def draw_grid():
    for row in range(10):
        if row % 3 == 0:
            thickness = 4  # Thicker line after every 3 rows
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
            num = player_board[row][col]
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


def draw_info():
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer_text = timer_font.render(f"Time: {minutes:02}:{seconds:02}", True, (0, 0, 0))
    mistake_text = timer_font.render(f"Mistakes: {mistakes}/{max_mistakes}", True, (255, 0, 0))
    # Place timer at top-left and mistakes just below it
    screen.blit(timer_text, (20, 10))
    screen.blit(mistake_text, (20, 42))


def draw_game_over(message):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((500, 600))
    overlay.set_alpha(180)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))
    game_over_text = font.render(message, True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(250, 300))
    screen.blit(game_over_text, text_rect)


def draw_number_bar():
    for num in range(1, 10):
        count = sum(row.count(num) for row in player_board)
        if count < 9 or num not in hidden_numbers:
            hidden_numbers.discard(num)  # Reappear if count drops below 9
            text = font.render(str(num), True, (0, 0, 0))
            x = OFFSET_X + (num - 1) * (CELL_SIZE + 5)
            y = NUMBER_BAR_Y
            screen.blit(text, (x, y))

# Check and hide numbers reached 9 times
def update_hidden_numbers():
    for num in range(1, 10):
        count = sum(row.count(num) for row in player_board)
        if count >= 9:
            hidden_numbers.add(num)
        elif count < 9:
            hidden_numbers.discard(num)


def handle_key(key):
    global mistakes, game_over
    if selected_cell and (pygame.K_1 <= key <= pygame.K_9 or pygame.K_KP1 <= key <= pygame.K_KP9):
        row, col = selected_cell
        if pygame.K_1 <= key <= pygame.K_9:  # Regular number keys
            value = key - pygame.K_1 + 1
        elif pygame.K_KP1 <= key <= pygame.K_KP9:  # Keypad number keys
            value = key - pygame.K_KP1 + 1
        player_board[row][col] = value
        update_hidden_numbers()
        if full_board[row][col] != value:
            incorrect_cells.add((row, col))
            mistakes += 1
            if mistakes >= 3:
                game_over = True
        else:
            incorrect_cells.discard((row, col))
        check_win()


def handle_click(pos):
    x, y = pos
    if OFFSET_X < x < OFFSET_X + GRID_SIZE and OFFSET_Y < y < OFFSET_Y + GRID_SIZE:
        col = (x - OFFSET_X) // CELL_SIZE
        row = (y - OFFSET_Y) // CELL_SIZE
        return row, col
    return None


def check_win():
    global game_over
    if all(player_board[row][col] == full_board[row][col] for row in range(9) for col in range(9)):
        game_over = True


def draw_game_over(message):
    overlay = pygame.Surface((500, 600))
    overlay.set_alpha(180)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))
    lines = message.split('\n')
    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 0, 0))
        text_rect = text.get_rect(center=(250, 280 + i * 60))
        screen.blit(text, text_rect)

def wait_with_exit(timeout):
    clock = pygame.time.Clock()
    start = time.time()
    while time.time() - start < timeout:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        clock.tick(30)


def restart_game():
    global player_board, incorrect_cells, mistakes, start_time, game_over
    _, game_board = generate_sudoku(num_remove=40)
    player_board = [list(row) for row in game_board]
    incorrect_cells.clear()
    mistakes, game_over = 0, False
    start_time = time.time()


def draw_controls():
    controls_text = desc_font.render("Ctrl+R to restart; Ctrl+Q to quit", True, (0, 0, 0))
    screen.blit(controls_text, (OFFSET_X, OFFSET_Y + GRID_SIZE + 70))


def main():
    print("Full Board (Solution):") # For testing purposes only
    print_board(full_board)

    global selected_cell, game_over
    running = True
    clock = pygame.time.Clock()  # Přidání časovače pro kontrolu FPS

    while running:
        screen.fill((255, 255, 255))
        draw_controls()
        draw_number_bar()
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Process events only if game is not over
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected_cell = handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        selected_cell = None
                    elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        restart_game()
                    elif event.key == pygame.K_q and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        pygame.quit()
                        exit()
                    else:
                        handle_key(event.key)
                        update_hidden_numbers()

        draw_selection()
        draw_numbers()
        draw_info()

        if not game_over and check_win():
            draw_game_over("Congratulations!\nYou Win!")
            pygame.display.flip()
            wait_with_exit(5)
            break

        if game_over:
            message = "Game Over!\nToo many mistakes." if mistakes >= max_mistakes else "Congratulations!\nYou Win!"
            draw_game_over(message)
            pygame.display.flip()
            wait_with_exit(5)
            break

        pygame.display.flip()  # Refreshes window
        clock.tick(30)  # Sets FPS on 30

    pygame.quit()


if __name__ == "__main__":
    main()
