from tkinter import * 
import random

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

root = Tk()

speed = 500

grid_line_color = 'gray'
background = 'black'

canvas_width = 240 
canvas_height = 300

square_side = 20
squares_width = int(canvas_width / square_side)
squares_height = int(canvas_height / square_side)

w = Canvas(root, width=canvas_width, height=canvas_height)
w.pack() 

grid: list 

pieces = {
    'square': {  
        'color': 'red', 'orientations': 
            [ '**\n**' ] 
    },
    't': { 
        'color': 'green', 'orientations': 
            ['***\n * ', '* \n**\n* ', ' * \n***', ' *\n**\n *'] 
    },
    'line': { 
        'color': 'yellow', 'orientations': 
            ['*\n*\n*\n*', '****', ] 
    },
    'left-l': { 
        'color': 'blue', 'orientations': 
            ['* \n* \n**', '  *\n***', '**\n *\n *',  '***\n*  '] 
    },
    'right-l': { 
        'color': 'orange', 'orientations': 
            [ ' *\n *\n**', '***\n  *', '**\n* \n* ',  '  *\n***'] 
    },
    's': { 
        'color': 'lawngreen', 'orientations': 
        [' **\n** ', '* \n**\n *'] 
    },
    'z': { 'color': 'purple', 'orientations': 
        [ '** \n **', ' *\n**\n* '] 
    },
}

active_piece_info: dict
active_piece_orientation_index: int
active_piece_orientation: str
active_piece_col: int
active_piece_row: int

def initialize_game():
    global grid
    grid = []
    for x in range(squares_height):
        grid.append(make_empty_row())
    start_new_piece()


def make_empty_row():
    line = []
    for y in range(squares_width):
        line.append('')
    return line 


def start_new_piece():
    global active_piece_row, active_piece_col, active_piece_info
    global active_piece_orientation, active_piece_orientation_index 

    active_piece_name = random.choice(list(pieces.keys()))
    active_piece_info = pieces[active_piece_name]
    active_piece_orientation_index = 0
    active_piece_orientation = active_piece_info['orientations'][active_piece_orientation_index]

    active_piece_col = int(squares_width / 2) - 2
    active_piece_row = 0


def key_press(event):
    global active_piece_col, active_piece_orientation, active_piece_orientation_index

    key = event.keysym   # the letter, or 'Up', 'Down', 'Left', 'Right' ... 
    if key == 'Left':
        if active_piece_col > 0:
            if can_move_piece(active_piece_row, active_piece_col - 1):
                active_piece_col -= 1
    
    elif key == 'Right':
        active_piece_width = len(active_piece_orientation.split('\n')[0])
        if active_piece_col + active_piece_width < squares_width:   # if not bump into wall...
            if can_move_piece(active_piece_row, active_piece_col + 1):   # or other set pieces
                active_piece_col += 1   
    
    elif key == 'Up':  # rotate 
        next_index = (active_piece_orientation_index + 1) % len(active_piece_info['orientations'])
        next_orientation = active_piece_info['orientations'][next_index]

        if can_move_piece(active_piece_row, active_piece_col, next_orientation):
            active_piece_orientation_index = (active_piece_orientation_index + 1) % len(active_piece_info['orientations'])
            active_piece_orientation = active_piece_info['orientations'][active_piece_orientation_index]
    
    elif key == 'r':
        initialize_game()


def move_active_piece():
    global active_piece_row
    if can_move_piece(active_piece_row + 1, active_piece_col):
        active_piece_row += 1
        return True
    else:
        set_piece()
        return False 


def set_piece():
    component_squares = active_piece_orientation.split('\n')
    for row_index, line in enumerate(component_squares):
        for col_index, square in enumerate(line):
            if square == '*':  # this is a part of the active piece
                row_loc = active_piece_row + row_index
                col_loc = active_piece_col + col_index
                grid[row_loc][col_loc] = active_piece_info['color']


def can_move_piece(next_row, next_col, next_orientation=None):

    if next_orientation:
        orientation = next_orientation
    else:
        orientation = active_piece_orientation

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
    return not can_move_piece(0, int(squares_width / 2))


def clear():
    w.create_rectangle(0, 0, canvas_width, canvas_height, fill=background)


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
                x = col_index * square_side
                y = row_index * square_side
                w.create_rectangle(x, y, x + square_side, y + square_side, fill=col)


def draw_active_piece(): 
    component_squares = active_piece_orientation.split('\n')

    for row_index, line in enumerate(component_squares):
        for col_index, square in enumerate(line):
            if square == '*':
                x = (active_piece_col + col_index) * square_side
                y = (active_piece_row + row_index) * square_side
                w.create_rectangle(x, y, x+square_side, y+square_side, fill=active_piece_info['color'])


def draw_grid():
    # horizontal lines
    for index, row in enumerate(grid):
        w.create_line(0, index*square_side, canvas_width, index*square_side, fill=grid_line_color)  # x1, y1, x2, y2

    # vertical lines 
    for index, col in enumerate(grid[0]):
        w.create_line(index*square_side, 0, index*square_side, canvas_height, fill=grid_line_color)


def game_loop():   
    
    if game_over():
        w.create_rectangle(0, canvas_height / 3, canvas_height, canvas_height / 3 * 2, fill='gray')
        w.create_text(int(canvas_width/2), int(canvas_height/2), text='Game Over\nPress R to restart', font="Courier 20 bold", fill='deeppink')

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



