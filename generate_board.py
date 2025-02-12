import random


def is_valid(board, row, col, num):
    """Checks if a number can be placed in the board."""
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    box_x, box_y = (col // 3) * 3, (row // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_y + i][box_x + j] == num:
                return False

    return True


def solve(board):
    """Solves Sudoku using backtracking."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)  # Shuffle numbers for variety
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def generate_full_board():
    """Generates a complete Sudoku board."""
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve(board)
    return board


def remove_numbers(board, num_remove=40):
    """Removes numbers to create a playable Sudoku puzzle."""
    board_copy = [row[:] for row in board]
    removed = 0

    while removed < num_remove:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board_copy[row][col] != 0:
            board_copy[row][col] = 0
            removed += 1

    return board_copy


def generate_sudoku(num_remove=40):
    """Generates a full Sudoku board and a playable board."""
    full_board = generate_full_board()
    game_board = remove_numbers(full_board, num_remove)
    return full_board, game_board
