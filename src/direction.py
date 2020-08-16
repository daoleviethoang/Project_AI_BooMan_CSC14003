import numpy as np

from enum import Enum
class Direction(Enum):
    LEFT = "l"
    RIGHT = "r"
    UP = "u"
    DOWN = "d"

def cell_to_coord(path, nrow):
    # (i, j)
    return [(cell % nrow, cell // nrow) for cell in path]

def coord_to_direction(path, start_x, start_y):
    # Các hướng đi
    u = Direction.UP.value
    d = Direction.DOWN.value
    l = Direction.LEFT.value
    r = Direction.RIGHT.value

    cur_x = start_x
    cur_y = start_y
    #1: r, 2: u, 3: l, 4: d  
    output = []
    for t in path:
        i, j = t
        if (i, j) == (cur_y, cur_x):
            continue
        if i > cur_x:
            output.append(d)
        elif i < cur_x:
            output.append(u)
        else:
            if j > cur_y:
                output.append(r)
            elif j < cur_y:
                output.append(l)


        cur_x = i
        cur_y = j

    return output


if __name__ == "__main__":
    
    path = [(2, 8), (2, 9), (2, 10), (2, 11), (3, 11), \
            (4, 11), (5, 11), (6, 11), (6, 12), (6, 13), (6, 14), (6, 15), (6, 16)]
    start_x = 2
    start_y = 8
 
    print(coord_to_direction(path, start_x, start_y))
