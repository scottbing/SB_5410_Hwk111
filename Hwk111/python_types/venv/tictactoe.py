# importing the required libraries
import pygame as pg
import sys
import time
import random
from pygame.locals import *

# declaring the global variables

# for storing the 'x' or 'o'
# value as character
XO = 'x'

MAX, MIN = 1000, -1000

# storing the WINNER's value at
# any instant of code
WINNER = None

# to check if the game is a DRAW
DRAW = None

# to set WIDTH of the game window
WIDTH = 400

# to set height of the game window
HEIGHT = 400

# to set background color of the
# game window
WHITE = (255, 255, 255)

# color of the straightlines on that
# WHITE game board, dividing board
# into 9 parts
LINE_COLOR = (0, 0, 0)

# setting up a 3 * 3 board in canvas
BOARD = [[None] * 3, [None] * 3, [None] * 3]

# setting fps manually
FPS = 30

# how many draws
DRAWS = 0

# how may minmax
MMX = 0

# maximum number of games played
MAX_GAMES = 200

# how many games
RAN = 0

# number of times minimax is called
# MMTIMES = 0

# this is used to track time
CLOCK = pg.time.Clock()

# this method is used to build the
# infrastructure of the display
SCREEN = pg.display.set_mode((WIDTH, HEIGHT + 100), 0, 32)

# loading the images as python object
INITIATING_WINDOW = pg.image.load("modified_cover.png")
X_IMG = pg.image.load("x_modified.png")
Y_IMG = pg.image.load("o_modified.png")

# resizing images
INITIATING_WINDOW = pg.transform.scale(INITIATING_WINDOW, (WIDTH, HEIGHT + 100))
X_IMG = pg.transform.scale(X_IMG, (80, 80))
O_IMG = pg.transform.scale(Y_IMG, (80, 80))


def game_initiating_window():
    """Draw the playing board"""
    # displaying over the screen
    SCREEN.blit(INITIATING_WINDOW, (0, 0))

    # updating the display
    pg.display.update()
    time.sleep(0.1)
    SCREEN.fill(WHITE)

    # flush old events from menu
    pg.event.clear()

    # DRAWing vertical lines
    pg.draw.line(SCREEN, LINE_COLOR, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
    pg.draw.line(SCREEN, LINE_COLOR, (WIDTH / 3 * 2, 0), (WIDTH / 3 * 2, HEIGHT), 7)

    # DRAWing horizontal lines
    pg.draw.line(SCREEN, LINE_COLOR, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
    pg.draw.line(SCREEN, LINE_COLOR, (0, HEIGHT / 3 * 2), (WIDTH, HEIGHT / 3 * 2), 7)
    draw_status()


# end def game_initiating_window():


def draw_status():
    """Setup to render the screen"""
    # getting the global variable DRAW
    # into action
    global DRAW, DRAWS, MMX, RAN

    if WINNER is None:
        message = XO.upper() + "'s Turn"
    else:
        if WINNER == 'x':
            RAN += 1
        else:
            MMX += 1
        message = WINNER.upper() + " won !"
    if DRAW:
        DRAWS += 1
        message = "Game Draw !"

    # setting a font object
    font = pg.font.Font(None, 30)

    # setting the font properties like
    # color and WIDTH of the text
    text = font.render(message, 1, (255, 255, 255))

    # copy the rendered message onto the board
    # creating a small block at the bottom of the main display
    SCREEN.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(WIDTH / 2, 500 - 50))
    SCREEN.blit(text, text_rect)
    pg.display.update()


# end def draw_status():


def check_win(ret_val: bool=False):
    """Check for a vertical, horizontal, or diagonal win"""
    global BOARD, WINNER, DRAW

    # DRAW is what hte ret_val cares about
    # moved these lines up from the bottom
    if (all([all(row) for row in BOARD]) and WINNER is None):
        DRAW = True

    if ret_val:
        if DRAW:
            DRAW = None
            return True
        else:
            return False

            # checking for winning rows
    for row in range(0, 3):
        if ((BOARD[row][0] == BOARD[row][1] == BOARD[row][2]) and (BOARD[row][0] is not None)):
            WINNER = BOARD[row][0]
            pg.draw.line(SCREEN, (250, 0, 0),
                         (0, (row + 1) * HEIGHT / 3 - HEIGHT / 6),
                         (WIDTH, (row + 1) * HEIGHT / 3 - HEIGHT / 6),
                         4)
            break

    # checking for winning columns
    for col in range(0, 3):
        if ((BOARD[0][col] == BOARD[1][col] == BOARD[2][col]) and (BOARD[0][col] is not None)):
            WINNER = BOARD[0][col]
            pg.draw.line(SCREEN, (250, 0, 0), ((col + 1) * WIDTH / 3 - WIDTH / 6, 0),
                         ((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT), 4)
            break

    # check for diagonal WINNERs
    if (BOARD[0][0] == BOARD[1][1] == BOARD[2][2]) and (BOARD[0][0] is not None):
        # game won diagonally left to right
        WINNER = BOARD[0][0]
        pg.draw.line(SCREEN, (250, 70, 70), (50, 50), (350, 350), 4)

    if (BOARD[0][2] == BOARD[1][1] == BOARD[2][0]) and (BOARD[0][2] is not None):
        # game won diagonally right to left
        WINNER = BOARD[0][2]
        pg.draw.line(SCREEN, (250, 70, 70), (350, 50), (50, 350), 4)

    # if (all([all(row) for row in BOARD]) and WINNER is None):
    #     DRAW = True
    draw_status()


# def check_win(ret_val=False):


def drawXO(row: int, col: int):
    """Draw the player's symbol on the board"""
    global BOARD, XO

    # for the first row, the image
    # should be pasted at a x coordinate
    # of 30 from the left margin
    if row == 1:
        posx = 30

    # for the second row, the image
    # should be pasted at a x coordinate
    # of 30 from the game line
    if row == 2:
        # margin or WIDTH / 3 + 30 from
        # the left margin of the window
        posx = WIDTH / 3 + 30

    if row == 3:
        posx = WIDTH / 3 * 2 + 30

    if col == 1:
        posy = 30

    if col == 2:
        posy = HEIGHT / 3 + 30

    if col == 3:
        posy = HEIGHT / 3 * 2 + 30

    # setting up the required board
    # value to display
    BOARD[row - 1][col - 1] = XO

    if (XO == 'x'):

        # pasting x_img over the screen
        # at a coordinate position of
        # (pos_y, posx) defined in the
        # above code
        SCREEN.blit(X_IMG, (posy, posx))
        XO = 'o'

    else:
        SCREEN.blit(O_IMG, (posy, posx))
        XO = 'x'
    pg.display.update()


# end def DRAWXO(row, col):


def user_click():
    """get coordinates of mouse click"""
    x, y = pg.mouse.get_pos()

    # get column of mouse click (1-3)
    if (x < WIDTH / 3):
        col = 1

    elif (x < WIDTH / 3 * 2):
        col = 2

    elif (x < WIDTH):
        col = 3

    else:
        col = None

    # get row of mouse click (1-3)
    if (y < HEIGHT / 3):
        row = 1

    elif (y < HEIGHT / 3 * 2):
        row = 2

    elif (y < HEIGHT):
        row = 3

    else:
        row = None

    # after getting the row and col,
    # we need to DRAW the images at
    # the desired positions
    if (row and col and BOARD[row - 1][col - 1] is None):
        global X0, WINNER, DRAW
        DRAWXO(row, col)
        check_win()
        if not DRAW and not WINNER:
            # computer only moves if click was valid and game not over
            computer_move()


# end def user_click():


def evaluate(b: list):
    """evaluate the current status of the board
    to make the next move"""
    player = 'o'
    opponent = 'x'
    for row in range(0, 3):
        if b[row][0] == b[row][1] and \
                b[row][1] == b[row][2]:
            if b[row][0] == player:
                return +10
            elif b[row][0] == opponent:
                return -10
    for col in range(0, 3):
        if b[0][col] == b[1][col] and \
                b[1][col] == b[2][col]:
            if b[0][col] == player:
                return +10
            elif b[0][col] == opponent:
                return -10
    # Checking for Diagonals for X or 0 victory.
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        if b[0][0] == player:
            return +10
        elif b[0][0] == opponent:
            return -10

    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
        if b[0][2] == player:
            return +10
        elif b[0][2] == opponent:
            return -10

    # Else if none of them have won then return 0
    return 0


# end def evaluate_BOARD(BOARD):


def minimax(BOARD: list, depth: int, is_max: bool, alpha: int, beta: int):
    """returns best move"""
    # global MMTIMES
    # MMTIMES += 1
    score = evaluate(BOARD)

    # either max won with 10 or min with —10
    if abs(score) == 10:
        return score
    # if this BOARD would be a DRAW
    if check_win(True) == True:
        return 0
    # if it is maximizers turn
    if is_max:
        return minmax(MIN, depth, max, is_max, 'o', alpha, beta)
    # else it is minimizer's turn
    else:
        return minmax(MAX, depth, min, is_max, 'x', alpha, beta)
    # end def minimax(BOARD, depth, is_max):


def minmax(top: int, depth: int, fn: (), is_max: bool, player: str, alpha: int, beta: int):
    """invokes the minimax function to make the next game move"""
    # repeat code from computer_move. You can clean this later
    best = top

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for row in range(1, 4):
        for col in range(1, 4):
            # check if cell is empty and valid
            if (BOARD[row - 1][col - 1] is None):
                # make the move
                BOARD[row - 1][col - 1] = player
                # compute evaluation function for this move

                val = minimax(BOARD, depth + 1, not is_max, alpha, beta)
                best = fn(best, val)
                if fn == max:
                    alpha = fn(alpha, best)
                elif fn == min:
                    beta = fn(beta, best)
                # undo the move
                BOARD[row - 1][col - 1] = None

                # prune further steps if necessary
                if beta <= alpha:
                    # since I am in a nested loop, I will return where thee tutorial breaks
                    return best
    return best
# def minmax(top, depth, fn, is_max, player, alpha, beta):

def random_move():
    valid_moves = []    # list of valid moves
    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for row in range(1, 4):
        for col in range(1, 4):
            # check if cell is empty and valid
            if (BOARD[row - 1][col - 1] is None):
                # create list of valid moves
                valid_moves.append((row - 1,col - 1))

    # choose a random move from the available valid moves(empty slots)
    move = random.randint(0, len(valid_moves)-1)
    global X0
    # extract the row col
    row, col = valid_moves[move]
    # make next move
    drawXO(row+1, col+1)
    check_win()
# end def random_move():

# This will return the best possible move for the player
def computer_move():
    """Makes the next board move based upon information
    received the minimax function"""
    global XO
    best_val = MIN
    best_move = (-1, -1)

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for row in range(1, 4):
        for col in range(1, 4):
            # check if cell is empty and valid
            if (BOARD[row - 1][col - 1] is None):
                # make the move
                BOARD[row - 1][col - 1] = XO
                # compute evaluation function for this move

                # TODO: Imlpement minimax
                move_val = minimax(BOARD, 0, False, MIN, MAX)
                # undo the move
                BOARD[row - 1][col - 1] = None

                # If the value of the current move is
                # more than the best value, then update
                # best
                if move_val > best_val:
                    best_move = (row, col)
                    best_val = move_val

    # perform move with the largest value
    drawXO(best_move[0], best_move[1])  # broken right now
    check_win()

    # global MMTIMES
    # print(MMTIMES)
    # mmtimes = 0


# end def computer_move():


def reset_game():
    """Reset the game board"""
    global BOARD, WINNER, XO, DRAW
    time.sleep(.1)
    XO = 'x'
    DRAW = False
    game_initiating_window()
    WINNER = None
    BOARD = [[None] * 3, [None] * 3, [None] * 3]


# end reset_game():


# driver Code
def main():
    """The python main() function.  Functions as
    the entry point to the application"""
    # initializing the pygame window
    pg.init()

    # setting up a nametag for the
    # game window
    pg.display.set_caption("My Tic Tac Toe")

    game_initiating_window()

    games = 0
    while (True):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                # user click()
                print("Draws: {0}, Minimax: {1}, Random: {2}". \
                      format(DRAWS, MMX, RAN))
                pg.quit()
                sys.exit()

        time.sleep(0.2)  # time to wait between move pairs
        random_move()  # make a random move
        if (WINNER or DRAW):  # check for end before next move
            games += 1
            if games >= MAX_GAMES:
                print("Draws: {0}, Minimax: {1}, Random: {2}, games {3}". \
                      format(DRAWS, MMX, RAN, games))
                pg.quit()
                sys.exit()
            reset_game()
        else:
            computer_move()  # minimax move
            if (WINNER or DRAW):
                games += 1
                if games >= MAX_GAMES:
                    print("Draws: {0}, Minimax: {1}, Random: {2}, games {3}". \
                          format(DRAWS, MMX, RAN, games))
                    pg.quit()
                    sys.exit()
                reset_game()
        pg.display.update()
        CLOCK.tick(FPS)


# end def main():


if __name__ == '__main__':
    main()
