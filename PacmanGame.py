import pygame, sys
from pygame.math import Vector2 as vec
import time
import random
import numpy as np

WIDTH, HEIGHT = 240,160
FPS = 60
TOP_BOTTOM_BUFFER = 50


BLACK = (0,0,0)
GREY = (107,107,107)


START_TEXT_SIZE = 16
START_FONT = 'arial black'

PLAY_START_POS = vec(0,0)

pygame.init()

class Pacman:
    def __init__(self, app, pos):
        self.app = app
        self.gird_pos = pos
        self.road = self.app.road_map()
        self.vision = []
        self.pac_location = pos
        self.pix_pos = self.get_pix_pos()
        self.step_move = vec(1,0)
        self.list_data = self.heuristic_allmap()
        self.food = vec(4,11)
        self.move_level_1, self.explored, self.timeEscape = self.Graph_Search_A_Star()
    def move(self, choose_move):
        if choose_move == 1: #left
            self.pix_pos += vec(-20,0)
            self.pac_location.x -= 1
        if choose_move == 2: #right
            self.pix_pos += vec(20,0)
            self.pac_location.x += 1
        if choose_move == 3: #down
            self.pix_pos += vec(0,-20)
            self.pac_location.y -= 1
        if choose_move == 4: #up
            self.pix_pos += vec(0,20)
            self.pac_location.y += 1
    def update(self):
        pass
    def draw(self):
        pygame.draw.circle(self.app.screen, (241,1,36), (int(self.pix_pos.x), int(self.pix_pos.y)),self.app.cell_width//2-2)
    def get_pix_pos(self):
        return (vec(((self.gird_pos.x + 1/2)*self.app.cell_width), ((self.gird_pos.y + 1/2)*self.app.cell_height)))
    def check_map(self, road):
        self.road = road
    def level_return(self, S_x, S_y):
        if S_x == -1 and S_y == 0:
            return 1
        elif  S_x == 1 and S_y == 0:
            return 2
        elif S_x == 0 and S_y == -1:
            return 3
        elif S_x == 0 and S_y == 1:
            return 4
    def level_1(self):
        X = 0
        self.move_level_1.pop(0)
        if not self.move_level_1:
            return X
        for i in self.move_level_1:
            S_x = int(i//(HEIGHT/20)) - self.pac_location.x
            S_y = int(i%(HEIGHT/20)) - self.pac_location.y
            X = self.level_return(int(S_x), int(S_y))
            break
        return X
    def pacman_play(self, level):
        if level == 1:
            self.vision = self.road
            return self.level_1()
        elif level == 2:
            pass
        elif level == 3:
            pass
        elif  level == 4:
            pass
    def heuristic(self, current, food):
        #mahatan
        return abs(current%int(HEIGHT/20) - food%int(HEIGHT/20)) + abs(current//int(HEIGHT/20) - food//int(HEIGHT/20))
    def isValid(self, row, col):
        if (row >= 0) and (row < HEIGHT/20) and (col >= 0) and (col < WIDTH/20):
            return True
        else:
            return False
    def isUnblock(self, vision, row, col):
        if vision[row][col] == 0 or vision[row][col] == 2:
            return True
        else:
            return False
    def isDestination(self, row, col, food):
        if(row == int(food.x) and col == int(food.y)):
            return True
        else:
            return False
    def heuristic_allmap(self):
        allmap = []
        for col in range(int(WIDTH/20)):
            for row in range(int(HEIGHT/20)):
                temp = []
                if self.isUnblock(self.road, row, col) == True and self.isValid(row, col) == True:
                        up = [row - 1,col]
                        down = [row + 1, col]
                        left = [row, col - 1]
                        right = [row, col + 1]
                        if self.isValid(up[0], up[1]) == True and self.isUnblock(self.road, up[0], up[1]) == True:
                            temp.append(int(HEIGHT/20)*up[1]+up[0])
                        if self.isValid(down[0], down[1]) == True and self.isUnblock(self.road, down[0], down[1]) == True:
                            temp.append(int(HEIGHT/20)*down[1]+down[0])
                        if self.isValid(left[0], left[1]) == True and self.isUnblock(self.road, left[0], left[1]) == True:
                            temp.append(int(HEIGHT/20)*left[1]+left[0])
                        if self.isValid(right[0], right[1]) == True and self.isUnblock(self.road, right[0], right[1]) == True:
                            temp.append(int(HEIGHT/20)*right[1]+right[0])
                        allmap.append(temp)
                else:
                    allmap.append([])
        return allmap
    def f_heuristic(self, node):
        return node[1]
    def next_node(self, current_node):
        return current_node[0][-1]
    def Graph_Search_A_Star(self):
        queue = []
        goal = int(self.food.x - 1) + int((HEIGHT/20)*int(self.food.y-1))
        queue.append(([0],self.heuristic(0,goal),0))
        explored = []
        visited = []
        timeEscape = 0
        for i in range(0,len(self.list_data)):
            visited.append(False)
        visited[0] = True
        while len(queue) > 0:
            queue = sorted(queue,key=self.next_node)
            queue = sorted(queue,key=self.f_heuristic)
            catch = queue.pop(0)
            g = catch[2]
            explored.append(catch[0][-1])
            timeEscape += 1
            visited[catch[0][-1]] = True
            if catch[0][-1] == goal:
                return catch[0], explored, timeEscape
            else:
                for x in self.list_data[catch[0][-1]]:
                    catch1 = catch[0].copy()
                    catch1.append(x)
                    if visited[x] == False:
                        visited[x] = True
                        queue.append((catch1,self.heuristic(x,goal) + g + 1,g + 1))
        return [], explored, timeEscape
''' #greedy di bui
    def move_a_star(self):
        food = vec(30,21) #vector do an
        current = self.pac_location
        p_vision = self.road.copy()
        p_vision_temp = self.road.copy()
        pacman_move = []
        while True:
            current_old = current
            matrix_temp = []
            index_max_heu = []
            flag = 0
            for i in [(-1,0),(1,0),(0,-1),(0,1)]:
                current = current + i
                if self.isDestination(int(current.x), int(current.y), food) == True:
                    pacman_move.append([int(current.x),int(current.y)])
                    return pacman_move
                if (self.isUnblock(p_vision, int(current.x), int(current.y)) == True and self.isValid(int(current.x), int(current.y)) == True):
                    h_new = self.heuristic(current, food)
                    p_vision_temp[int(current.x)][int(current.y)] = h_new
                    matrix_temp.append(h_new)
                    index_max_heu.append([int(current.x), int(current.y)])
                    flag = flag + 1
                current = current_old
            current = vec(index_max_heu[np.argmin(matrix_temp)][0],index_max_heu[np.argmin(matrix_temp)][1])
            if ([int(current.x),int(current.y)] in pacman_move) == True and flag == 1:
                p_vision[int(current_old.x)][int(current_old.y)] = 1
            pacman_move.append([int(current.x),int(current.y)])
    def A_Star_Seacrh(self, p_vision):
        while True:
            pass
'''
class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = 20 #(1 ô là 20, co the tinh theo WIDTH)
        self.cell_height = 20 #()
        self.matrixRoad = []
        self.pacman = Pacman(self, PLAY_START_POS)
        self.X = 0
        #self.load()

    def run(self):
        self.matrixRoad = self.road_map()
        self.pacman.check_map(self.matrixRoad)
        while self.running:
            self.X = self.pacman.pacman_play(1)
            #X = random.randint(1,4)
            if self.X == 0:
                print('End Game')
                return None
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            if self.state == 'playing':
                self.playing_events()
                self.playing_draw()
                self.playing_update(self.X)
                time.sleep(0.5)
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

 #   def draw_text(self,words, screnn,pos, size, colour, font_name, centered = False):
 #       font = pygame.font.SysFont(font_name, size)
 #       text = font.render(words, False, colour)
 #       text_size = text.get_size()
 #       pos[0] = pos[0] - text_size[0]//2
 #       pos[1] = pos[1] - text_size[1]//2
 #       screnn.blit(text, pos)

   # def load(self):
    #    self.background = pygame.image.load('maze.png')
     #   self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.screen, GREY, (x*self.cell_width, 0), (x*self.cell_width,HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.screen, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))


    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.state = 'playing'
    def start_update(self):
        pass
    def start_draw(self):
        self.screen.fill(BLACK)
        #self.draw_text('PUSH SPACE BAR',self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE, (170,132,58), START_FONT, centered = True)
        #self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH//2, HEIGHT//2+100], START_TEXT_SIZE, (33,137,156), START_FONT, centered = True)
        pygame.display.update()



    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    def playing_draw(self):
        self.screen.fill(BLACK)
        #self.screen.blit(self.background, (0,0))
        self. draw_grid()
        self.pacman.draw()
        pygame.display.update()
    def playing_update(self, move):
        self.pacman.move(move)
        #self.pacman.move(2)

    def road_map(self):
        file = open("matrixRoad.txt", 'r')
        Y = []
        X = file.readline().split(" ")
        measure = [int(e) for e in X]
        for line in file:
            Y.append([int(n) for n in line.strip().split(' ')])
        return np.array(Y)
'''
    def test(self):
        X = self.pacman.heuristic_allmap()
        path_return, explored, timeEscape = self.pacman.Graph_Search_A_Star()
        print("The time to escape the maze:",timeEscape)
        print("The list of explored nodes:",explored)
        print("The list of nodes on the path found:",path_return)
       # print(self.pacman.level_1(self.road_map()))
       '''
       
app = App()
app.run()
#answer = input('wrong')

#app = App()
#app.test()
