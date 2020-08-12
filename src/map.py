import tkinter
import pygame

SCREEN_HEIGHT, SCREEN_WIDTH = (512, 1024)
BLOCK_SIZE = 30
DOT_SIZE = 4

from enum import Enum
class Color(Enum):
    AMBER = (255, 160, 0)
    BLACK = (0, 0, 0)
    BLUE = (25, 118, 210)
    BLUE_GREY = (69, 90, 100)
    BROWN = (93, 64, 55)
    CYAN = (0, 151, 167)
    DEEP_ORANGE = (230, 74, 25)
    DEEP_PURPLE = (81, 45, 168)
    GREEN = (56, 142, 60)
    GREY = (97, 97, 97) 
    IDINGO = (48, 63, 159)
    LIGHT_BLUE = (2, 136, 209)
    LIGHT_GREEN = (104, 159, 56)
    LIME = (175, 180, 43)
    ORANGE = (245, 124, 0)
    PURPLE = (123, 31, 162)
    PINK = (194, 24, 91)
    RED = (211, 47, 47)
    TEAL = (0, 121, 107)
    WHITE = (255, 255, 255)
    YELLOW = (251, 192, 45)

FOOD_COLOR = Color.BLACK.value
WALL_COLOR = Color.GREY.value
ROAD_COLOR = Color.WHITE.value

ROAD = 0
WALL = 1
FOOD = 2
GHOST = 3

class map():

    def __init__(self, screen, grid2d, start_y, pacman_x, pacman_y):
        
        self.screen = screen
        self.grid_2d = grid2d
        self.pacman_x = pacman_x
        self.pacman_y = pacman_y
        # self.start_x = start_x
        self.start_y = start_y
    
        self.pacman_block = pygame.sprite.Group()
        self.wall_blocks = pygame.sprite.Group()
        self.ghost_blocks = pygame.sprite.Group()
        self.food_blocks = pygame.sprite.Group()

        for i, row in enumerate(self.grid_2d):
            for j, item in enumerate(row):
                x, y = self.to_screen_coord(i, j)
                if item == WALL:
                    wall_obj = wall_graphic(x, y, height=BLOCK_SIZE, width=BLOCK_SIZE)
                    self.wall_blocks.add(wall_obj)
                elif item == FOOD:
                    food_obj = food_graphic(x, y, height=BLOCK_SIZE, width=BLOCK_SIZE)
                    self.food_blocks.add(food_obj)
                ###  
                
    def to_screen_coord(self, i, j) -> tuple:
        x = j * BLOCK_SIZE
        y = self.start_y + i * BLOCK_SIZE
        return x, y
    
    """
    Get the total size of the map
    return a pair (width, height)
    """
    @staticmethod
    def total_screen_size(grid_2d, start_y=0) -> tuple:
        ## Để ý trường hợp grid_2d is None
        n_rows = len(grid_2d)
        n_cols = len(grid_2d[0])
        height = BLOCK_SIZE * (n_rows + start_y)
        width = BLOCK_SIZE * n_cols
        return width, height
        

    def draw_map(self):
        self.screen.fill(ROAD_COLOR)

        # --- Draw the game here ---
        self.wall_blocks.draw(self.screen)
        # draw_enviroment(screen)
        self.food_blocks.draw(self.screen)

        # screen.blit(self.player.image, self.player.rect)
        #text=self.font.render("Score: "+(str)(self.score), 1,self.RED)
        #screen.blit(text, (30, 650))
        # Render the text for the score
        # text = self.font.render("Score: " + str(self.score), True, GREEN)
        # Put the text on the screen
        # screen.blit(text,[120,20])
            
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    
"""

"""
class character_animation():

    """
    animaiton_img: một tấm ảnh biểu diễn animation 
                    Kích thước tấm ảnh sẽ là (n * height, n * width) với n là số tấm ảnh con sẽ cắt ra để biểu diễn animation
    (height, width): chiều dài gốc của một tấm ảnh đơn
    """
    def __init__(self, animation_img, height, width):

        # một list object các hình khi chạy sẽ cho ra animation
        self.animation_img = animation_img
        self.animations = to_animation_list(self.animation_img, height, width)

        # Index đến tấm hình hiện tại trong self.animations
        self.current_img = 0
        self.clock = 0

    def get_current_image(self):
        return self.animations[self.current_img]

    def get_animation_list(self):
        return self.animations.copy()

    def get_animation_len(self):
        return len(self.animations)

    @staticmethod
    def to_animation_list(animation_img, height, width)->str:
        animations = []
        full_height = animation_img.get_height()
        full_width = animation_img.get_width()

        for y in range(0, full_height, height):
            for x in range(0, full_width, width):
                # blank image
                image = pygame.Surface((width, height)).convert()
                # Vẽ đè animation_img vào image
                image.blit(animation_img, (0,0), (x, y, width, height))
                # image.set_colorkey((0,0,0))
                animations.append(image)
        return animations

    def update(self, fps=30):
        step = 30 // fps
        l = range(1, 30, step)
        
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            # Increase index
            self.index += 1
            if self.index == len(self.animations):
                self.index = 0


class pacman_graphic(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    
    eaten = False
    game_over = False

    '''
    (init_x, init_x): tọa độ của pac-man khi mới bắt đầu game
    img_path: đường dẫn file ảnh pac-man
    color_key: ảnh nền đồ họa pac-man
    '''
    def __init__(self, init_x, init_y, img_path='player.png', color_key=ROAD_COLOR):
        pygame.sprite.Sprite._init__(self)

        # Ảnh gốc
        self.image = pygame.image.load(img_path).convert()
        self.image.set_colorkey(color_key)
        
        # Ảnh hiện tại
        self.current_image = self.image

        # Rectangle object
        self.rect = self.image.get_rect()

        # position
        self.rect.topleft = (init_x, init_y)

        # walk animations objects
        animation_img = pygame.image.load("walk.png").convert()
        left_flipped = pygame.transform.flip(animation_img, xbool=True, ybool=False)
        up_flipped = pygame.transform.rotate(animation_img, angle=90)
        down_flipped = pygame.transform.rotate(up_flipped, angle=180)

        self.right_animation = character_animation(animation_img, height=BLOCK_SIZE, width=BLOCK_SIZE)
        self.left_animation = character_animation(left_flipped, height=BLOCK_SIZE, width=BLOCK_SIZE)
        self.up_animation = character_animation(up_flipped, height=BLOCK_SIZE, width=BLOCK_SIZE)
        self.down_animation = character_animation(down_flipped, height=BLOCK_SIZE, width=BLOCK_SIZE)

import math
class food_graphic(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, colorkey=FOOD_COLOR):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.color = colorkey
        
        # self.image.set_colorkey(Color.BLACK.value)
        self.image.fill(ROAD_COLOR)


        center = int(math.sqrt(2) / 2 * BLOCK_SIZE)
        # center_pos = x + center, y + center
        # pygame.draw.circle(self.image, self.color, (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2), 5)
        pygame.draw.ellipse(self.image, colorkey,(center/2, center/2, DOT_SIZE, DOT_SIZE))

        self.rect = self.image.get_rect()
        self.rect.topleft = x, y


class wall_graphic(pygame.sprite.Sprite):

    def __init__(self, x, y, height, width, colorkey=WALL_COLOR):
        pygame.sprite.Sprite.__init__(self)

        # Set the background color and set it to be transparent
        self.image = pygame.Surface((width,height))
        self.image.fill(colorkey)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

def main():

    grid_2d = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 2, 1, 0, 1, 0, 2, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1], 
        [1, 2, 1, 2, 1, 0, 2, 1, 2, 2, 2, 2, 1, 0, 0, 1, 0, 1, 0, 1], 
        [1, 0, 1, 1, 1, 0, 2, 1, 2, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1], 
        [1, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    # Initialize all imported pygame modules
    pygame.init()

    # Set the screen size
    print(map.total_screen_size(grid_2d))
    screen = pygame.display.set_mode(map.total_screen_size(grid_2d))

    # Set the current window caption
    pygame.display.set_caption("BOOMAN")
    
    #Loop until the user clicks the close button.
    closed_window = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()


    map_obj = map(screen, grid_2d, start_y=0, pacman_x=0, pacman_y=0)
    # screen.

    done = False
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop

        map_obj.draw_map()
        clock.tick(30)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()

if __name__ == '__main__':
    main()
