import pygame, sys
from pygame.math import Vector2 as vec
import time
import random
import numpy as np

from map import *
import map as m

# CONFIGURATION FOR DEBUGGING PURPOSE
FORCE_TO_MOVE = True # Bắt con pacman phải đi mặc dù thức ăn quá xa

class Pacman:
    def __init__(self, map_obj, pos):
        self.map_obj = map_obj
        self.map_nrow = map_obj.grid_2d.shape[0]
        self.map_ncol = map_obj.grid_2d.shape[1]

        self.grid_pos = pos # tính theo i, j
        self.road = self.map_obj.grid_2d
        # self.vision = []
        self.pac_location = pos
        self.pix_pos = self.get_pix_pos()
        self.list_data = self.heuristic_allmap() # adjacency list

    def get_pix_pos(self):
        return (vec(((self.grid_pos.x + 1/2)*m.BLOCK_SIZE), \
                ((self.grid_pos.y + 1/2)*m.BLOCK_SIZE)))
    
    def check_map(self, road):
        self.road = road
    
    """
    current, food: theo cell index, không phải tọa độ
    """
    def heuristic(self, current, food):
        #mahatan
        return abs(current % self.map_nrow - food % self.map_nrow) + abs(current//self.map_nrow - food//self.map_nrow)

    def isValid(self, row:int, col:int):
        return (row >= 0) and (row < self.map_nrow) and (col >= 0) and (col < self.map_ncol)

    def isUnblock(self, vision, row:int, col:int):
        return self.map_obj.ghost_map[row, col] != GHOST \
                and (vision[row, col] != WALL)

    def isDestination(self, row:int, col:int, food: vec):
        return (row == int(food.x) and col == int(food.y))
    

    """
    Trả về một danh sách các cạnh kề nhau
    """
    def heuristic_allmap(self):
        allmap = []
        for col in range(self.map_ncol):
            for row in range(self.map_nrow):

                temp = []
                if self.isUnblock(self.road, row, col) and self.isValid(row, col):
                        up = [row - 1,col]
                        down = [row + 1, col]
                        left = [row, col - 1]
                        right = [row, col + 1]

                        if self.isValid(up[0], up[1]) and self.isUnblock(self.road, up[0], up[1]):
                            temp.append(self.map_nrow * up[1] + up[0])

                        if self.isValid(down[0], down[1]) and self.isUnblock(self.road, down[0], down[1]):
                            temp.append(self.map_nrow * down[1] + down[0])

                        if self.isValid(left[0], left[1]) and self.isUnblock(self.road, left[0], left[1]):
                            temp.append(self.map_nrow * left[1] + left[0])

                        if self.isValid(right[0], right[1]) and self.isUnblock(self.road, right[0], right[1]):
                            temp.append(self.map_nrow * right[1] + right[0])
                        allmap.append(temp)

                else:

                    allmap.append([])
        return allmap    

    def f_heuristic(self, node):
        return node[1]

    def next_node(self, current_node):
        return current_node[0][-1]

    def Graph_Search_A_Star(self, goal_x, goal_y):
        queue = []
        
        # Các node trong A_start tính theo số thứ tự của LAB01
        goal = int(goal_y) + self.map_nrow * int(goal_x)
        start = int(self.pac_location.y) + self.map_nrow * int(self.pac_location.x)

        # (node, f, g)
        queue.append(([start], self.heuristic(start,goal), 0))
        explored = []
        visited = []
        timeEscape = 0

        for i in range(0, len(self.list_data)):
            visited.append(False)
        # visited[0] = True # Node 0 không có bị visited # may cho bài này node 0 luôn là WALL
        visited[start] = True

        while len(queue) > 0:
            queue = sorted(queue,key=self.next_node)
            queue = sorted(queue,key=self.f_heuristic)

            catch = queue.pop(0)
            g = catch[2]
            explored.append(catch[0][-1])

            timeEscape += 1
            visited[catch[0][-1]] = True

            if catch[0][-1] == goal:
                # print("!", explored)
                # print(catch[0])
                return catch[0], explored, timeEscape

            else:

                for x in self.list_data[catch[0][-1]]:
                    catch1 = catch[0].copy()
                    catch1.append(x)
                    if visited[x] == False:
                        visited[x] = True
                        queue.append((catch1, self.heuristic(x,goal) + g + 1, g + 1))
        # print(explored)
        return [], explored, timeEscape


# TODO: Chuyển hàm này vào class một class nào đó?
def level1_2(map_obj: map_graphic, pacman_moves: list):

    if map_obj.game_over:
        return
    
    # Pacman ---------------------------
    if pacman_moves is not None or len(pacman_moves) > 0:
        if not map_obj.pacman_block.is_moving():
            ### XÓA DÒNG NÀY KHI GHÉP THUẬT TOÁN LEVEL 1
            ### pacman_moves.append(map_obj.pacman_block.random_moves(map_obj))
            if len(pacman_moves) > 0:
                has_moves = True
                direction = pacman_moves.pop(0)
                map_obj.pacman_block.turn(direction)
        
        map_obj.pacman_block.update(map_obj)
        hit_food_blocks = pygame.sprite.spritecollide(map_obj.pacman_block, map_obj.food_blocks, True)

        if len(hit_food_blocks) > 0:
            map_obj.pacman_block.score += SCORE_PER_FOOD
            food_x, food_y = hit_food_blocks[0].rect.topleft
            print("FOOD (x, y): ", food_x, food_y)

            food_i, food_j = map_obj.to_cell_coord(food_x, food_y)
            print("FOOD (i, j): ", food_i, food_j)
            map_obj.grid_2d[food_i, food_j] = WALL
        

    hit_ghost_blocks = pygame.sprite.spritecollide(map_obj.pacman_block, map_obj.ghost_blocks,True)
    
    if len(hit_ghost_blocks) > 0:
        map_obj.game_over = True

    # Pac đã đi hết đoạn đường cần đi
    if len(pacman_moves) == 0 and not map_obj.pacman_block.is_moving():
        map_obj.game_over = True
        
    # Ghosts ----------------------------
    # for ghost in map_obj.ghost_objs:
    #    if not ghost.is_moving():
    #        ghost.turn(ghost.random_moves(map_obj))

    # map_obj.ghost_blocks.update(map_obj)

from pygame.math import Vector2 as vec
def run_game1(grid_2d: np.ndarray, pacman_i, pacman_j, init_yet=False):
    
    # Initialize all imported pygame modules
    print("HELLO")
    if not init_yet:
        pygame.init()

    # get and set the system screen size
    screen_width, screen_height = set_screen_size(grid_2d)
    # print(total_screen_size(grid_2d))
    screen = pygame.display.set_mode((screen_width, screen_height + m.BLOCK_SIZE))

    # Set the current window caption
    pygame.display.set_caption(WINDOW_TITLE)
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #Loop until the user clicks the close button.
    closed_window = False
    start_y = m.BLOCK_SIZE

    print(f"Block size: {m.BLOCK_SIZE}")
    print(f"start_y: {start_y}")

    map_obj = map_graphic(screen, grid_2d, start_y, pacman_i=pacman_i, pacman_j=pacman_j)
    pacman = Pacman(map_obj, vec(pacman_j, pacman_i))    
    
    # ----------------------
    # Tính toán đường đi của pacman
    foods = np.where(map_obj.grid_2d == FOOD)
    should_go = True
    if not np.size(foods) == 0:
        food_x = foods[1][0]
        food_y = foods[0][0]

        nrow, _ = map_obj.grid_2d.shape
        path, _, _ = pacman.Graph_Search_A_Star(food_x, food_y)
        # Quyết định chọn đi hay không:
        if not FORCE_TO_MOVE:
            should_go = len(path) - 2 <= SCORE_PER_FOOD
        
        pacman_moves = coord_to_direction(cell_to_coord(path, nrow), start_x=pacman_j, start_y=pacman_i)
    else: 
        path = []
        pacman_moves = []
        should_go = False
    
    print(f"Path: {len(path)} | {path}")
    print(f"Moves: {len(pacman_moves)} | {pacman_moves}")

    # Game Loop -----------
    done = False
    game_over = False
    while not done:

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True

        if should_go:
            level1_2(map_obj, pacman_moves)

        map_obj.draw_map()

        if map_obj.game_over or not should_go:
            game_over = True
            break

        # Tăng/giảm frame speed ở đây
        clock.tick(GAME_FPS)

    print(map_obj)
    print("SCORE: ", map_obj.pacman_block.score)

    if game_over:
        pygame.time.wait(5000)

    if not init_yet:
        pygame.quit()

from readfile import *
def test():
    
    size, grid_2d, start = readfile('input/1/input21.txt')
    size = np.array(size)
    grid_2d = np.array(grid_2d)
    start = np.array(start)

    grid_2d, size, start = check_fence(grid_2d, size, start)
    print("MAP SIZE: ", len(grid_2d))
    run_game1(grid_2d, pacman_i=start[0], pacman_j=start[1])

def main(level, path):

    size, grid_2d, start = readfile(path)
    size = np.array(size)
    grid_2d = np.array(grid_2d)
    start = np.array(start)

    grid_2d, size, start = check_fence(grid_2d, size, start)
    print("MAP SIZE: ", len(grid_2d))
    print(f"LEVEL  : {level}")
    print(f"PATH   : {path}")
    level1_2_str = [1, 2, "1", "2", "LEVEL1", "LEVEL2"]

    if level in level1_2_str:
        print(f"PLAY {level}")
        run_game1(grid_2d, pacman_i=start[0], pacman_j=start[1])
    

import sys
if __name__ == '__main__':
    ##### VUI LÒNG CHUYỂN THƯ MỤC LÀM VIỆC Project_AI_BooMan_CSC14003 ĐỂ CÓ THỂ ĐỌC FILE ẢNH ĐƯỢC
    # main()
    argv = sys.argv
    if len(argv) <= 1:
        test()
    else:
        main(argv[1], argv[2])
