from random import shuffle, randrange
WALL = 1
ROAD = 0

# cols = w * 2 + 1
# rows = h * 2
def make_maze(w = 16, h = 8):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    print(s)
    s = ""
    def walk(x, y):
        vis[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)
 
    walk(randrange(w), randrange(h))
    
    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    
    maze_blocks = []
    
    for (h, v) in zip(hor, ver):
        # row1 = [ROAD if i != 0 and item == "+  " else WALL for i, item in enumerate(h)]
        # row2 = [ROAD if i != 0 and item == "   " else WALL for i, item in enumerate(v)]
        row1 = []
        for i, item in enumerate(h):
            if len(v) == 0:
                continue

            if item == "+--":
                row1.append(WALL)
                row1.append(WALL)
            elif item == "+  ":
                row1.append(WALL)
                row1.append(ROAD)               
            else:
                row1.append(WALL)

        row2 = []
        for i, item in enumerate(v):
            if item == "|  ":
                row2.append(WALL)
                row2.append(ROAD)
            elif item == "   ":
                row2.append(ROAD)
                row2.append(ROAD)               
            else:
                row2.append(WALL)
        if len(row1) != 0:
            maze_blocks.append(row1)
        if len(row2) != 0:
            maze_blocks.append(row2)

    maze_blocks_str = "\n".join(" ".join(str(col) for col in row) for row in maze_blocks)
    
    rows = len(maze_blocks)
    cols = len(maze_blocks[0]) ## 

    return s, f"{rows} {cols}\n{maze_blocks_str}"
 
if __name__ == '__main__':
    s, blocks = make_maze(w=30, h=20)
    print(s)
    print(blocks)