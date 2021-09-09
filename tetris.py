from tkinter import * 
import random

"""
more stuff that could be added
* press down/space to drop peice
* display score based on rows cleared
* levels, which are progessively faster. speed up game based on level

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

def make_empty_row():
    line = []
    for y in range(squares_width):
        line.append('')
    return line 


grid: list 

w = Canvas(root, width=canvas_width, height=canvas_height)

w.pack() 


pieces = {
    'square': { 'color': 'red', 'orientations': [
        '**\n**'
    ] },
    't': { 'color': 'green', 'orientations': [
        '***\n * ', '* \n**\n* ', ' * \n***', ' *\n**\n *'
    ] },
    'line': { 'color': 'yellow', 'orientations': [
        '*\n*\n*\n*', '****',
    ] },
    # 'left-l': { color: 'blue', orientations: [] },
    # 'right-l': { color: 'orange', orientations: [] },
    # 's': { color: 'pink', orientations: [] },
    # 'z': { color: 'purple', orientations: [] },
}


# active_piece_name = random.choice(list(pieces.keys()))
# active_piece_info = pieces[active_piece_name]
# active_piece_orientation_index = 0
# active_piece_orientation = active_piece_info['orientations'][active_piece_orientation_index]
# active_piece_col = int(squares_width / 2)
# active_piece_row = 0

active_piece_name: str
active_piece_info: dict
active_piece_orientation_index: int
active_piece_orientation: str
active_piece_col: int
active_piece_row: int

# print(active_piece_col, active_piece_row)

def start_new_piece():
    # return false if can't start? 
    global active_piece_row, active_piece_col, active_piece_name, active_piece_info
    global active_piece_orientation, active_piece_orientation_index 

    active_piece_name = random.choice(list(pieces.keys()))
    active_piece_info = pieces[active_piece_name]
    active_piece_orientation_index = 0
    active_piece_orientation = active_piece_info['orientations'][active_piece_orientation_index]

    active_piece_col = int(squares_width / 2)
    active_piece_row = 0


def restart():
    global grid
    grid = []
    for x in range(squares_height):
        grid.append(make_empty_row())
    start_new_piece()

restart()

def key_press(event):

    global active_piece_col, active_piece_orientation, active_piece_orientation_index

    key = event.keysym   # the letter, or 'Up', 'Down', 'Left', 'Right' ... 
    print(key)
    if key == 'Left':
        if active_piece_col > 0:
            if can_move_piece(active_piece_row, active_piece_col-1):
                active_piece_col -= 1
        # don't bump into set pieces, use  
    elif key == 'Right':
        active_piece_width = len(active_piece_orientation.split('\n')[0])
        print(active_piece_width, active_piece_col, squares_width)
        if active_piece_col + active_piece_width < squares_width:   # if not bump into wall...
            if can_move_piece(active_piece_row, active_piece_col+1):   # or other set pieces
                active_piece_col += 1   
        # TODO don't bump into set pieces 
    elif key == 'Up':  # rotate 

        next_index = (active_piece_orientation_index + 1) % len(active_piece_info['orientations'])
        next_orientation = active_piece_info['orientations'][next_index]

        if can_move_piece(active_piece_row, active_piece_col, next_orientation):
            active_piece_orientation_index = (active_piece_orientation_index + 1) % len(active_piece_info['orientations'])
            active_piece_orientation = active_piece_info['orientations'][active_piece_orientation_index]
    
    elif key == 'r':
        restart()


def draw_grid():
    # horizontal lines
    for index, row in enumerate(grid):
        w.create_line(0, index*square_side, canvas_width, index*square_side, fill=grid_line_color)  # x1, y1, x2, y2

    # vertical lines 
    for index, col in enumerate(grid[0]):
        w.create_line(index*square_side, 0, index*square_side, canvas_height, fill=grid_line_color)


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
            # print(col_index, square)
            if square == '*':
                x = (active_piece_col + col_index) * square_side
                y = (active_piece_row + row_index) * square_side
                w.create_rectangle(x, y, x+square_side, y+square_side, fill=active_piece_info['color'])


def move_active_piece():
    global active_piece_row
    # print(active_piece_row, active_piece_col)
    if can_move_piece(active_piece_row + 1, active_piece_col):
        print('move piece down')
        active_piece_row += 1
    
        return True
    else:
        print('setting piece in place')
        set_piece()
        return False 


def set_piece():
    component_squares = active_piece_orientation.split('\n')
    for row_index, line in enumerate(component_squares):
        for col_index, square in enumerate(line):
            if square == '*':  # this is a part of the active piece
                print('filling in square')
                print(grid)
                row_loc = active_piece_row + row_index
                col_loc = active_piece_col + col_index
                
                # print(row_loc, active_piece_row, row_index)
                # print(col_loc, active_piece_col, col_index)
                
                # grid[row_loc][col_index] = active_piece_info['color']
                print('setting at', row_loc, col_loc)
                grid[row_loc][col_loc] = active_piece_info['color']


def can_move_piece(next_row, next_col, next_orientation=None):
    # TODO if we move to this position, will it hit bottom or other set pieces? 
    # no rotate is different to landed on the bottom/other pieces 

    print(next_row, next_col)

    if next_orientation:
        orientation = next_orientation
    else:
        orientation = active_piece_orientation

    piece_height = len(orientation.split('\n'))
    print(f'{piece_height=}')
    # piece_width = len(active_piece_orientation[0])

    if next_row + piece_height > len(grid):  
        return False 
    # if next_row < 0:
    #     return False  # is this possible?
    
    # if next_col < 0:
    #     return False

    # if next_col >= len(grid[0]):
    #     return False

    # TODO differentiate between can't rotate or can't move into wall, vs. has fallen and should be stuck

    component_squares = orientation.split('\n')
    for row_index, line in enumerate(component_squares):
        for col_index, square in enumerate(line):
            if square == '*':  # this is a part of the active piece
                # does it overlap set piece OR wall or base? 
                row_loc = next_row + row_index
                col_loc = next_col + col_index
                print(row_loc,col_loc)
                try:
                    if grid[row_loc][col_loc]:
                        return False 
                except IndexError:  # ewwwww
                    return False
    return True



def remove_complete_rows():
    # this works?? 
    rows_rem = 0 

    index_to_examine = len(grid) - 1

    while index_to_examine > 0:
        row = grid[index_to_examine]
        if all(row):  # is color in each square
            grid.pop(index_to_examine)
            rows_rem -= 1
            grid.insert(0, make_empty_row())
            draw_all()
           
        index_to_examine -= 1

    return rows_rem  # for future score
            

def game_over():
    return not can_move_piece(0, int(squares_width / 2))


def clear():
    w.create_rectangle(0, 0, canvas_width, canvas_height, fill=background)


def draw_all():
    clear()
    draw_grid()
    draw_current_pieces()
    draw_active_piece()


def game_loop():
    
    print('loop')
    was_moved = move_active_piece()

    draw_all()

    remove_complete_rows()

    if not was_moved:
        start_new_piece()
    
    # # FIXME
    if game_over():
        print('game is over')
        return 
    else:
        root.after(speed, game_loop)



w.create_line(0, 40, 400, 40, fill='#4510bb')
root.bind('<Key>', key_press)

root.after(speed, game_loop)
root.mainloop()


