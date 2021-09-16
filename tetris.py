"""

Tkinter - no PyGame, no classes, not much math 

Fix the rotation point for shapes, some look weird on rotation - T ?
Pieces can move L, R too fast if key held down
Occasional index out of bounds error in can_move_piece
When a row is completed and cleared, the active piece is drawn in it's set location, then removed on the next tick

more things that could be added
* press down/space to drop piece
* display score based on rows cleared
* levels, which are progessively faster. speed up game based on level
* bug - checking for game over - if new piece doesn't fit, it is not drawn and gap shown at top of screen
"""

from tkinter import Tk, Canvas
import random


root = Tk()


speed = 500

GRID_LINE_COLOR = 'gray'
BACKGROUND_COLOR = 'black'

CANVAS_WIDTH = 240 
CANVAS_HEIGHT = 300

SQUARE_SIDE = 20
SQUARES_WIDTH = int(CANVAS_WIDTH / SQUARE_SIDE)
SQUARES_HEIGHT = int(CANVAS_HEIGHT / SQUARE_SIDE)

w = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
w.pack() 

grid: list 


pieces = {
    'square': {  
        'color': 'red', 'orientations': 
            ['**\n**'] 
    },
    't': { 
        'color': 'green', 'orientations': 
            ['***\n * ', '* \n**\n* ', ' * \n***', ' *\n**\n *'] 
    },
    'line': { 
        'color': 'yellow', 'orientations': 
            ['*\n*\n*\n*', '****'] 
    },
    'left-l': { 
        'color': 'blue', 'orientations': 
            ['* \n* \n**', '  *\n***', '**\n *\n *',  '***\n*  '] 
    },
    'right-l': { 
        'color': 'orange', 'orientations': 
            [' *\n *\n**', '***\n  *', '**\n* \n* ',  '  *\n***'] 
    },
    's': { 
        'color': 'lawngreen', 'orientations': 
            [' **\n** ', '* \n**\n *'] 
    },
    'z': {
        'color': 'purple', 'orientations': 
            ['** \n **', ' *\n**\n* '] 
    },
}

ACTIVE_PIECE_INFO: dict
ACTIVE_PIECE_ORIENTATION_INDEX: int
ACTIVE_PIECE_ORIENTATION: str
ACTIVE_PIECE_COL: int
ACTIVE_PIECE_ROW: int

def initialize_game():
    """ Set up grid, and create first piece """
    global grid
    grid = []
    for x in range(SQUARES_HEIGHT):
        grid.append(make_empty_row())
    start_new_piece()


def make_empty_row():
    line = []
    for y in range(SQUARES_WIDTH):
        line.append('')
    return line 


def start_new_piece():
    global ACTIVE_PIECE_ROW, ACTIVE_PIECE_COL, ACTIVE_PIECE_INFO
    global ACTIVE_PIECE_ORIENTATION, ACTIVE_PIECE_ORIENTATION_INDEX 

    active_piece_name = random.choice(list(pieces.keys()))
    ACTIVE_PIECE_INFO = pieces[active_piece_name]
    ACTIVE_PIECE_ORIENTATION_INDEX = 0
    ACTIVE_PIECE_ORIENTATION = ACTIVE_PIECE_INFO['orientations'][ACTIVE_PIECE_ORIENTATION_INDEX]

    ACTIVE_PIECE_COL = int(SQUARES_WIDTH / 2) - 2
    ACTIVE_PIECE_ROW = 0


def key_press(event):

    """ Examine key press event from user, and decide what action to take """
    global ACTIVE_PIECE_COL, ACTIVE_PIECE_ORIENTATION, ACTIVE_PIECE_ORIENTATION_INDEX

    key = event.keysym   # the letter, or 'Up', 'Down', 'Left', 'Right' ... 
    if key == 'Left':
        if ACTIVE_PIECE_COL > 0:
            if can_move_piece(ACTIVE_PIECE_ROW, ACTIVE_PIECE_COL - 1):
                ACTIVE_PIECE_COL -= 1
    
    elif key == 'Right':
        active_piece_width = len(ACTIVE_PIECE_ORIENTATION.split('\n')[0])
        if ACTIVE_PIECE_COL + active_piece_width < SQUARES_WIDTH:   # if not bump into wall...
            if can_move_piece(ACTIVE_PIECE_ROW, ACTIVE_PIECE_COL + 1):   # or other set pieces
                ACTIVE_PIECE_COL += 1   
    
    elif key == 'Up':  # rotate 
        next_index = (ACTIVE_PIECE_ORIENTATION_INDEX + 1) % len(ACTIVE_PIECE_INFO['orientations'])
        next_orientation = ACTIVE_PIECE_INFO['orientations'][next_index]

        if can_move_piece(ACTIVE_PIECE_ROW, ACTIVE_PIECE_COL, next_orientation):
            ACTIVE_PIECE_ORIENTATION_INDEX = (ACTIVE_PIECE_ORIENTATION_INDEX + 1) % len(ACTIVE_PIECE_INFO['orientations'])
            ACTIVE_PIECE_ORIENTATION = ACTIVE_PIECE_INFO['orientations'][ACTIVE_PIECE_ORIENTATION_INDEX]
    
    elif key == 'r':  # If the R key is pressed, restart the game 
        initialize_game()


def move_active_piece():
    """ Move the active piece down one row if possible.
    Return true if the piece can be moved down """
    global ACTIVE_PIECE_ROW
    if can_move_piece(ACTIVE_PIECE_ROW + 1, ACTIVE_PIECE_COL):
        ACTIVE_PIECE_ROW += 1
        return True
    else:
        set_piece()
        return False 


def set_piece() :
    component_squares = ACTIVE_PIECE_ORIENTATION.split('\n')
    for row_index, line in enumerate(component_squares):
        for col_index, square in enumerate(line):
            if square == '*':  # this is a part of the active piece
                row_loc = ACTIVE_PIECE_ROW + row_index
                col_loc = ACTIVE_PIECE_COL + col_index
                grid[row_loc][col_loc] = ACTIVE_PIECE_INFO['color']


def can_move_piece(next_row, next_col, next_orientation=None):

    if next_orientation:
        orientation = next_orientation
    else:
        orientation = ACTIVE_PIECE_ORIENTATION

    piece_height = len(orientation.split('\n'))
    
    if next_row + piece_height > len(grid):    # reached bottom of screen 
        return False 

    component_squares = orientation.split('\n')
    for row_index, line in enumerate(component_squares):
        for col_index, square in enumerate(line):
            if square == '*':  # this is a part of the active piece
                # does it overlap set piece? 
                row_loc = next_row + row_index
                col_loc = next_col + col_index
                if grid[row_loc][col_loc]:  
                    return False 
                    
    return True


def remove_complete_rows():
    rows_removed = 0 

    index_to_examine = len(grid) - 1

    while index_to_examine > 0:
        row = grid[index_to_examine]
        if all(row):  # is color entered in each square? then this is a complete row
            grid.pop(index_to_examine)
            rows_removed -= 1
            grid.insert(0, make_empty_row())
            draw_all()
           
        index_to_examine -= 1

    return rows_removed  # for future score feature, based on the number of rows removed. 
            

def game_over():
    # A new piece added at the start, if it can't move, then the board must be full. 
    return not can_move_piece(0, int(SQUARES_WIDTH / 2))


def clear():
    w.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill=BACKGROUND_COLOR)


def draw_all(show_active_peice=True):
    clear()
    draw_grid()
    draw_current_pieces()
    if show_active_peice:
        draw_active_piece()

# rows are horizontal. e.g Row 3 defines a position on the Y axis
# cols are vertical. Col 2 defines a position on the x axis. 
def draw_current_pieces():
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            if col:
                x = col_index * SQUARE_SIDE
                y = row_index * SQUARE_SIDE
                w.create_rectangle(x, y, x + SQUARE_SIDE, y + SQUARE_SIDE, fill=col)


def draw_active_piece(): 
    component_squares = ACTIVE_PIECE_ORIENTATION.split('\n')

    for row_index, line in enumerate(component_squares):
        for col_index, square in enumerate(line):
            if square == '*':
                x = (ACTIVE_PIECE_COL + col_index) * SQUARE_SIDE
                y = (ACTIVE_PIECE_ROW + row_index) * SQUARE_SIDE
                w.create_rectangle(x, y, x+SQUARE_SIDE, y+SQUARE_SIDE, fill=ACTIVE_PIECE_INFO['color'])


def draw_grid():
    # horizontal lines
    for index, _ in enumerate(grid):
        w.create_line(0, index*SQUARE_SIDE, CANVAS_WIDTH, index*SQUARE_SIDE, fill=GRID_LINE_COLOR)  # x1, y1, x2, y2

    # vertical lines 
    for index, _ in enumerate(grid[0]):
        w.create_line(index*SQUARE_SIDE, 0, index*SQUARE_SIDE, CANVAS_HEIGHT, fill=GRID_LINE_COLOR)


def game_loop():   
    
    if game_over():
        w.create_rectangle(0, CANVAS_HEIGHT / 3, CANVAS_HEIGHT, CANVAS_HEIGHT / 3 * 2, fill='gray')
        w.create_text(int(CANVAS_WIDTH/2), int(CANVAS_HEIGHT/2), text='Game Over\nPress R to restart', font="Courier 20 bold", fill='deeppink')

    else:
        was_moved_down = move_active_piece()

        draw_all()

        remove_complete_rows()

        if not was_moved_down:
            start_new_piece()
        

    root.after(speed, game_loop)   
  

        
root.bind('<Key>', key_press)  # key event handlers
    
initialize_game()   # sets up game data

root.after(speed, game_loop)  # starts game loop
root.mainloop()



