import pygame
import numpy as np
import random

# Initialize pygame
pygame.init()

# Board settings
size_of_board = 900
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = (53, 28, 117)  # Red color for symbol X
symbol_O_color = (201, 0, 118)  # Blue color for symbol O
green_color = (50, 164, 0)  # Green color for scores
bg_color_choices = [
    (245, 245, 220), (250, 240, 230), (255, 250, 205), (253, 245, 230), (255, 228, 196),
    (248, 248, 231), (255, 248, 220), (255, 235, 205), (253, 245, 232), (250, 235, 215),
    (255, 239, 213), (240, 230, 140), (255, 218, 185), (255, 228, 181), (244, 164, 96),
    (255, 222, 173), (255, 215, 0), (252, 230, 201), (255, 228, 225), (244, 164, 96)
]

# Set up the game window
window = pygame.display.set_mode((size_of_board, size_of_board))
pygame.display.set_caption('Hey! Play Tic-Tac-Toe 😉')

# Game variables
board_status = np.zeros(shape=(3, 3))
player_X_turns = True
player_X_starts = True
reset_board = False
game_over = False
tie = False
X_wins = False
O_wins = False
X_score = 0
O_score = 0
tie_score = 0
font = pygame.font.SysFont('cmr', 60, bold=True)
score_font = pygame.font.SysFont('cmr', 40, bold=True)
small_font = pygame.font.SysFont('cmr', 20, bold=True)


def initialize_board():
    window.fill((255, 255, 255))  # Clear the window
    for i in range(2):
        pygame.draw.line(window, (0, 0, 0), ((i + 1) * size_of_board / 3, 0),
                         ((i + 1) * size_of_board / 3, size_of_board), 3)
        pygame.draw.line(window, (0, 0, 0), (0, (i + 1) * size_of_board / 3),
                         (size_of_board, (i + 1) * size_of_board / 3), 3)


def change_board_color():
    bg_color = random.choice(bg_color_choices)
    window.fill(bg_color)


def play_again():
    global board_status, player_X_starts, player_X_turns, reset_board, game_over, tie, X_wins, O_wins
    board_status = np.zeros(shape=(3, 3))
    player_X_turns = player_X_starts
    reset_board = False
    game_over = False
    tie = False
    X_wins = False
    O_wins = False


def reset_game():
    global X_score, O_score, tie_score
    change_board_color()
    initialize_board()
    play_again()
    X_score = 0
    O_score = 0
    tie_score = 0


def draw_O(logical_position):
    grid_position = convert_logical_to_grid_position(logical_position)
    pygame.draw.circle(window, symbol_O_color, grid_position, symbol_size, symbol_thickness)


def draw_X(logical_position):
    grid_position = convert_logical_to_grid_position(logical_position)
    pygame.draw.line(window, symbol_X_color, (grid_position[0] - symbol_size, grid_position[1] - symbol_size),
                     (grid_position[0] + symbol_size, grid_position[1] + symbol_size), symbol_thickness)
    pygame.draw.line(window, symbol_X_color, (grid_position[0] - symbol_size, grid_position[1] + symbol_size),
                     (grid_position[0] + symbol_size, grid_position[1] - symbol_size), symbol_thickness)


def display_gameover():
    global X_score, O_score, tie_score, reset_board
    if X_wins:
        X_score += 1
        text = 'Winner: Player 1 (X)'
        color = symbol_X_color
    elif O_wins:
        O_score += 1
        text = 'Winner: Player 2 (O)'
        color = symbol_O_color
    else:
        tie_score += 1
        text = 'It\'s a tie'
        color = (128, 128, 128)

    window.fill((255, 255, 255))
    gameover_text = font.render(text, True, color)
    window.blit(gameover_text, (size_of_board / 2 - gameover_text.get_width() / 2, size_of_board / 3))

    score_text = 'Scores'
    score_text_surface = score_font.render(score_text, True, green_color)
    window.blit(score_text_surface, (size_of_board / 2 - score_text_surface.get_width() / 2, 5 * size_of_board / 8))

    score_text = 'Player 1 (X): ' + str(X_score)
    score_text_surface = score_font.render(score_text, True, green_color)
    window.blit(score_text_surface, (size_of_board / 2 - score_text_surface.get_width() / 2, 3 * size_of_board / 4))

    score_text = 'Player 2 (O): ' + str(O_score)
    score_text_surface = score_font.render(score_text, True, green_color)
    window.blit(score_text_surface, (size_of_board / 2 - score_text_surface.get_width() / 2, 3 * size_of_board / 4 + 50))

    score_text = 'Tie: ' + str(tie_score)
    score_text_surface = score_font.render(score_text, True, green_color)
    window.blit(score_text_surface, (size_of_board / 2 - score_text_surface.get_width() / 2, 3 * size_of_board / 4 + 100))

    reset_text = 'Click to play again'
    reset_text_surface = small_font.render(reset_text, True, (128, 128, 128))
    window.blit(reset_text_surface, (size_of_board / 2 - reset_text_surface.get_width() / 2, 15 * size_of_board / 16))


def convert_logical_to_grid_position(logical_position):
    logical_position = np.array(logical_position, dtype=int)
    return (size_of_board / 3) * logical_position + size_of_board / 6


def convert_grid_to_logical_position(grid_position):
    grid_position = np.array(grid_position)
    return np.array(grid_position // (size_of_board / 3), dtype=int)


def is_grid_occupied(logical_position):
    if board_status[logical_position[0]][logical_position[1]] == 0:
        return False
    else:
        return True


def is_winner(player):
    player = -1 if player == 'X' else 1

    # Three in a row
    for i in range(3):
        if board_status[i][0] == board_status[i][1] == board_status[i][2] == player:
            return True
        if board_status[0][i] == board_status[1][i] == board_status[2][i] == player:
            return True

    # Diagonals
    if board_status[0][0] == board_status[1][1] == board_status[2][2] == player:
        return True
    if board_status[0][2] == board_status[1][1] == board_status[2][0] == player:
        return True

    return False


def is_tie():
    r, c = np.where(board_status == 0)
    return len(r) == 0


def is_gameover():
    global X_wins, O_wins, tie
    X_wins = is_winner('X')
    if not X_wins:
        O_wins = is_winner('O')

    if not O_wins:
        tie = is_tie()

    return X_wins or O_wins or tie


def handle_click(event):
    global player_X_turns, reset_board, game_over
    grid_position = [event.pos[0], event.pos[1]]
    logical_position = convert_grid_to_logical_position(grid_position)

    if not reset_board:
        if player_X_turns:
            if not is_grid_occupied(logical_position):
                draw_X(logical_position)
                board_status[logical_position[0]][logical_position[1]] = -1
                player_X_turns = not player_X_turns
        else:
            if not is_grid_occupied(logical_position):
                draw_O(logical_position)
                board_status[logical_position[0]][logical_position[1]] = 1
                player_X_turns = not player_X_turns

        if is_gameover():
            display_gameover()
    else:
        change_board_color()
        initialize_board()  # Add this line to redraw the board
        play_again()
        reset_board = False


# Game loop
running = True
change_board_color()
initialize_board()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event)

    pygame.display.flip()

# Quit the game
pygame.quit()
