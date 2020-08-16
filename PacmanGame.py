import pygame, sys
from pygame.math import Vector2 as vec
import time
import random
import numpy as np

WIDTH, HEIGHT = 380,400
FPS = 60
TOP_BOTTOM_BUFFER = 50


BLACK = (0,0,0)
GREY = (107,107,107)


START_TEXT_SIZE = 16
START_FONT = 'arial black'

#PLAY_START_POS = vec(18,17)

pygame.init()

class Pacman:
    def __init__(self, app, pos):
        self.app = app
        self.gird_pos = pos
        self.road = self.app.map
        self.vision = []
        self.pac_location = pos
        self.pix_pos = self.get_pix_pos()
        self.step_move = vec(1,0)
        self.list_data = self.heuristic_allmap(self.road,int(WIDTH/20),int(HEIGHT/20)).copy()
        self.food = vec(18,1)
        self.save_shadow = self.create_save_shadow()
        self.move_level_1, self.explored, self.timeEscape = self.Graph_Search_A_Star()
    def move(self, choose_move):
        if choose_move == 1: #left
            self.pix_pos += vec(-20,0)
            self.pac_location.x -= 1
        if choose_move == 2: #right
            self.pix_pos += vec(20,0)
            self.pac_location.x += 1
        if choose_move == 3: #up
            self.pix_pos += vec(0,-20)
            self.pac_location.y -= 1
        if choose_move == 4: #down
            self.pix_pos += vec(0,20)
            self.pac_location.y += 1
        if choose_move == 5:
            self.pix_pos += vec(0,0)
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
        elif S_x == 0 and S_y == 0:
            return 5
    def level_1(self):
        X = 0
        if not self.move_level_1:
            return X
        for i in self.move_level_1:
            S_x = int(i//(HEIGHT/20)) - self.pac_location.x
            S_y = int(i%(HEIGHT/20)) - self.pac_location.y
            X = self.level_return(int(S_x), int(S_y))
            self.move_level_1.pop(0)
            break
        return X
    def pacman_play(self, level):
        if level == 1 or level == 2:
            self.vision = self.road
            return self.level_1()
        elif level == 3:
            return self.level_3()
            pass
        elif  level == 4:
            pass
    def heuristic(self, current, food):
        #mahatan
        return abs(current%int(HEIGHT/20) - food%int(HEIGHT/20)) + abs(current//int(HEIGHT/20) - food//int(HEIGHT/20))
    def isValid(self, row, col, height, width):
        if (row >= 0) and (row < height) and (col >= 0) and (col < width):
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
    def heuristic_allmap(self, map,width, height):
        allmap = []
        for col in range(width):
            for row in range(int(height)):
                temp = []
                if self.isUnblock(map, row, col) == True and self.isValid(row, col, height, width) == True:
                        up = [row - 1,col]
                        down = [row + 1, col]
                        left = [row, col - 1]
                        right = [row, col + 1]
                        if self.isValid(up[0], up[1], height, width) == True and self.isUnblock(map, up[0], up[1]) == True:
                            temp.append(int(height)*up[1]+up[0])
                        if self.isValid(down[0], down[1], height, width) == True and self.isUnblock(map, down[0], down[1]) == True:
                            temp.append(int(height)*down[1]+down[0])
                        if self.isValid(left[0], left[1], height, width) == True and self.isUnblock(map, left[0], left[1]) == True:
                            temp.append(int(height)*left[1]+left[0])
                        if self.isValid(right[0], right[1], height, width) == True and self.isUnblock(map, right[0], right[1]) == True:
                            temp.append(int(height)*right[1]+right[0])
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
        goal = int(self.food.x) + int((HEIGHT/20)*int(self.food.y))
        start = int(self.pac_location.x) + int((HEIGHT/20)*int(self.pac_location.y))
        queue.append(([start],self.heuristic(start,goal),0))
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
    def create_save_shadow(self):
        temp = []
        save_shadow = []
        for i in range(int(HEIGHT/20)):
            for j in range(int(WIDTH/20)):
                temp.append(-1)
            save_shadow.append(temp)
        return save_shadow
    def get_shadow(self):
        map_shadow = []
        flag = 0
        check = 0
        for row in range(int(self.pac_location.x) - 3, int(self.pac_location.x)+4):
            temp = []
            for col in range(int(self.pac_location.y) -3, int(self.pac_location.y) +4):
                if self.isValid(row,col, HEIGHT/20, WIDTH/20) == True and col >= (int(self.pac_location.y) - flag) and col <= (int(self.pac_location.y) + flag):
                    if(self.pac_location.x == row and self.pac_location.y == col and self.road[row][col] == 2):
                        self.road[row][col] = 0
                    temp.append(self.road[row][col])
                else:
                    temp.append(-1)
            if flag <= 3 and check == 0:
                flag += 1
            if flag > 3:
                flag = flag - 1
                check = 1
            if check == 1:
                flag -= 1
            map_shadow.append(temp)
        return map_shadow
    def get_food(self, map_shadow):
        food = []
        for row in range(len(map_shadow)):
            for col in range(len(map_shadow[0])):
                if(map_shadow[row][col] == 2):
                    food.append([row,col])
        return food
    def check_monster(self, map_shadow):
        for row in range(len(map_shadow)):
            for col in range(len(map_shadow[0])):
                check = 0
                if(map_shadow[row][col] == 3):
                    if(row == 3 and col == 0):
                        if  map_shadow[row][col + 1] == 3:
                            map_shadow[row][col] = 1
                        else:
                            map_shadow[row][col] = 1
                            map_shadow[row][col + 1] = 1
                    elif(row == 3 and col == len(map_shadow[0]) - 1):
                        if map_shadow[row][col - 1] == 3:
                            map_shadow[row][col] = 1
                        else:
                            map_shadow[row][col] = 1
                            map_shadow[row][col - 1] = 1
                    elif(col == 3 and row == 0):
                        if map_shadow[row + 1][col] == 3:
                            map_shadow[row][col] = 1
                        else:
                            map_shadow[row+1][col] = 1
                            map_shadow[row][col] = 1
                    elif(col == 3 and row == len(map_shadow[0]) - 1):
                        if map_shadow[row - 1][col] == 3: 
                            map_shadow[row][col] = 1
                        else:
                            map_shadow[row][col] = 1
                            map_shadow[row - 1][col] == 1
                    else:
                        if row == 3 and col == 2:
                            check = 1
                        elif(row == 2 and col == 3):
                            check = 2
                        elif(row == 3 and col == 4):
                            check = 3
                        elif(row == 4 and col == 3):
                            check = 4
                        map_shadow[row][col] = 1
                        if(map_shadow[row][col+1] != -1 and map_shadow[row][col+1] != 3 and check != 1):
                            map_shadow[row][col+1] = 1
                        if(map_shadow[row][col-1] != -1 and map_shadow[row][col-1] != 3 and check != 3):
                            map_shadow[row][col-1] = 1
                        if(map_shadow[row+1][col] != -1 and map_shadow[row+1][col] != 3 and check != 2):
                            map_shadow[row+1][col] = 1
                        if(map_shadow[row-1][col] != -1 and map_shadow[row-1][col] != 3 and check != 4):
                            map_shadow[row-1][col] = 1
        return map_shadow   
    #cap nhap bong pacman
    #cap nhap bong cua ma
    #cap nhap do an
    #bat dau tinh trong bong

    def Breadth_First_Search(self, list_data, start, food):
        queue = []
        queue.append([start])
        explored = []
        visited = []
        timeEscape = 0
        for i in range(0,len(list_data)):
            visited.append(False)
        visited[0] = True
        while len(queue) > 0:
            catch = queue.pop(0)
            explored.append(catch[-1])
            timeEscape += 1
            visited[catch[-1]] = True
            if catch[-1] == food:
                return catch, explored, timeEscape
            else:
                for x in list_data[catch[-1]]:
                    catch1 = catch.copy()
                    catch1.append(x)
                    if visited[x] == False:
                        visited[x] = True
                        queue.append(catch1)
        return [], explored, timeEscape

    def get_w_food(self, set_food):
        data_food = []
        for x in set_food:
            data_food.append(int(x[0]) + int((7)*int(x[1])))
        return data_food
    def check_around(self, map_shadow):
        X = []

        if(map_shadow[3][2] == 0):
            X.append([3,2])
        if(map_shadow[3][4] == 0):
            X.append([3,4])
        if(map_shadow[2][3] == 0):
            X.append([2,3])
        if(map_shadow[4][3] == 0):
            X.append([4,3])
        if len(X) != 0:
            i = random.randint(0,len(X) - 1)
            return X[i]
        return []
    def set_limit(self, map_shadow):
        limit = []
        flag = 0
        check = 0
        for row in range(7):
            for col in range(7):
                if(col == (3 - flag) or col == (3 + flag)):
                    if map_shadow[row][col] != 1 and map_shadow[row][col] != -1:
                        limit.append([row,col])
            if flag <= 3 and check == 0:
                flag += 1
            if flag > 3:
                flag = flag - 1
                check = 1
            if check == 1:
                flag -= 1
        return limit
    def path_level_3(self):
        self.road = [[self.road[j][i] for j in range(len(self.road))] for i in range(len(self.road[0]))]
        map_shadow = self.check_monster(self.get_shadow()).copy()
        #map_shadow = [[map_shadow1[j][i] for j in range(len(map_shadow1))] for i in range(len(map_shadow1[0]))] 
        set_food = self.get_food(map_shadow).copy()
        data_level3 = self.heuristic_allmap(map_shadow, 7, 7).copy()
        start = 3 + 7*3
        data_food = self.get_w_food(set_food).copy()
        Y = []
        check = 0
        set_path_limit = []
        if not data_food:
            check = 1
            s_limit = self.set_limit(map_shadow)
            d_limit = self.get_w_food(s_limit)
            for i in d_limit:
                path_return, explored, timeEscape = self.Breadth_First_Search(data_level3,start, i)
                set_path_limit.append(path_return)
            list2 = [e for e in set_path_limit if e]
            if len(list2) > 1:
                list_path = sorted(list2, key = len)
                return list2[0]
            else:
                print('end game')
                return []
            #X = self.check_around(map_shadow).copy()
            #goal = int(X[0]) + int((7)*int(X[1]))
            #path_return,explored,timeEscape = self.Breadth_First_Search(data_level3, start, goal)
            return path_return
        else:
            for i in data_food:
                path_return,explored,timeEscape = self.Breadth_First_Search(data_level3,start, i)
                Y.append(path_return)
        queue1 = [e for e in Y if e]
        if len(queue1) > 1:
            queue = sorted(queue1, key = len)
            return queue[0]
        if len(Y[0]) > 0:
            return Y[0]
        elif check != 1:
            return explored
    def level_3(self):
        path_temp = self.path_level_3().copy()
        if len(path_temp) > 1:
            path_temp.pop(0)
        else:
            return 5
        for i in path_temp:
            S_x = int(i%7) - 3
            S_y = int(i//7) - 3
            X = self.level_return(int(S_x), int(S_y))
            return X
        '''
 #greedy di bui
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
        self.size, self.map, self.start = self.readfile()
        self.pacman = Pacman(self, self.start)
        self.X = 0
        #self.load()

    def run(self):
        self.pacman.check_map(self.map)
        #print(self.pacman.explored)
        while self.running:
            self.X = self.pacman.pacman_play(3)
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
    
    def readfile(self):
        f = open("matrixRoad.txt", 'r')#mo file
        a = f.readline()
        size = a.split(' ')
        for i in range(len(size)):
            size[i] = size[i].rstrip('\n')
            size[i] = int(size[i])
        map=[]
        #print(size)
        while True:
            file = f.readline()
            if not file:
                break
            temp = file.split(' ')
            for i in range(len(temp)):
                temp[i] = temp[i].rstrip('\n')
                temp[i] = int(temp[i])
            map.append(temp)
        start = map.pop(-1)
        #print(map)
        #print(c)
        f.close()

        return vec(size[0], size[1]), np.array(map), vec(start[0], start[1])
    def test(self):
        A= self.pacman.path_level_3()
        print(A)
       # print(self.pacman.level_1(self.road_map()))
'''
    def road_map(self):
        file = open("matrixRoad.txt", 'r')
        Y = []
        X = file.readline().split(" ")
        measure = [int(e) for e in X]
        for line in file:
            Y.append([int(n) for n in line.strip().split(' ')])
        return np.array(Y)
'''
       
app = App()
app.run()
#answer = input('wrong')

#app = App()
#app.test()
