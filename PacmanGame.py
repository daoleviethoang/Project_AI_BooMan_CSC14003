import pygame, sys
from pygame.math import Vector2 as vec
import time
import random
import numpy as np

WIDTH, HEIGHT = 960,640
FPS = 60
TOP_BOTTOM_BUFFER = 50


BLACK = (0,0,0)
GREY = (107,107,107)


START_TEXT_SIZE = 16
START_FONT = 'arial black'

PLAY_START_POS = vec(20,20)

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
        self.move_level_1 = self.move_a_star()
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
        for i in self.move_level_1:
            S_x = i[0] - self.pac_location.x
            S_y = i[1] - self.pac_location.y
            self.move_level_1 = np.delete(self.move_level_1,0,0)
            return self.level_return(int(S_x), int(S_y))
        return 0
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
        return abs(current.x - food.x) + abs(current.y - food.y)
    def isValid(self, row, col):
        if (row >= 0) and (row < HEIGHT/20) and (col >= 0) and (col < WIDTH/20):
            return True
        else:
            return False
    def isUnblock(self, vision, row, col):
        if vision[row][col] == 0:
            return True
        else:
            return False
    def isDestination(self, row, col, food):
        if(row == int(food.x) and col == int(food.y)):
            return True
        else:
            return False
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

                current = current_old
            current = vec(index_max_heu[np.argmin(matrix_temp)][0],index_max_heu[np.argmin(matrix_temp)][1])
            if ([int(current.x),int(current.y)] in pacman_move) == True:
                p_vision[int(current_old.x)][int(current_old.y)] = 1
            pacman_move.append([int(current.x),int(current.y)])
    def A_Star_Seacrh(self, p_vision):
        while True:
            pass
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
                time.sleep(10)
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
    #def test(self):
       # print(self.pacman.level_1(self.road_map()))
app = App()
app.run()
#answer = input('wrong')

#app = App()
#app.test()