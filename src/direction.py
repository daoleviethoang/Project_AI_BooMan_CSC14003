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
    
    path = [(0, 1), (0, 2), (0, 3), (1, 3), (1, 2)]
    start_x = 0
    start_y = 0

    print(coord_to_direction(path, start_x, start_y))
