import tkinter
import pygame
import numpy as np
import random
from enum import Enum
from direction import *

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

COLOR_LIST = [e.value for e in Color]
COLOR_LIST.remove(Color.WHITE.value)

### CONFIGURATION
WINDOW_TITLE = "BOOMAN"
GAME_FONT = "res/font.ttf"
SCREEN_HEIGHT, SCREEN_WIDTH = (576, 800)
DYNAMIC_SCREEN_SIZE = True  # Tự động thay đổi kích thước phù hợp với map
BLOCK_SIZE = 30             # Giá trị BLOCK_SIZE có thể bị thay đổi khi DYNAMIC_SCREEN_SIZE = True
DOT_SIZE = BLOCK_SIZE // 6
GAME_FPS = 60

FOOD_COLOR = Color.BLACK.value
WALL_COLOR = random.choice(COLOR_LIST)
ROAD_COLOR = Color.WHITE.value
TEXT_COLOR = Color.BLUE.value

GHOST_IMG = "res/slime" + random.choice(["1", "2", "3", "4"]) + ".png"
PACMAN_IMG = "res/pacman.png"
PACMAN_ANIMATION = ["res/walk1.png", "res/walk2.png", "res/walk3.png"]
PACMAN_STEP_COST = 1
PACMAN_ANIMATION_SPEED = 5
SCORE_PER_FOOD = 20
STEP_LEN = 1

ROAD = 0
WALL = 1
FOOD = 2
GHOST = 3
PACMAN = 4

import tkinter as tk
def set_screen_size(grid_2d):

    global BLOCK_SIZE
    global DOT_SIZE
    # get and set the system screen size
    # graphic.BLOCK_SIZE

    if DYNAMIC_SCREEN_SIZE:
        display_info  = pygame.display.Info()
        # max_width, max_height = display_info.current_w, display_info.current_h
        nrow, ncol = grid_2d.shape
        print(f"{nrow} x {ncol}")
        root = tk.Tk()
        max_width = root.winfo_screenwidth()
        max_height = root.winfo_screenheight()

        print(f"MAX WIDTH, MAX HEIGHT: ({max_width} {max_height})")
        expected_height = int(max_height * 0.8)
        BLOCK_SIZE = expected_height // nrow

        if nrow <= 20:
            BLOCK_SIZE = 30
        # elif nrow <= 40:
        #     BLOCK_SIZE = 20
        # else:
        #     BLOCK_SIZE = 10

        screen_width, screen_height = map_graphic.total_screen_size(grid_2d, BLOCK_SIZE)
        print(f"MAP WIDTH, MAP HEIGHT: ({screen_width} {screen_height})")
        print(f"BLOCK_SIZE: {BLOCK_SIZE}")
        DOT_SIZE = BLOCK_SIZE // 6
    else:
        screen_width, screen_height = (SCREEN_WIDTH, SCREEN_HEIGHT)

    return screen_width, screen_height


class map_graphic():

    def __init__(self, screen, grid_2d: np.ndarray, start_y: int, pacman_i: int, pacman_j: int):

        self.screen = screen
        self.game_over = False

        self.grid_2d = grid_2d.copy()

        # vị trí của GHOST, WALL
        # tách ra thành 2 map riêng biệt
        # vì trong một ô có thể vừa có GHOST vừa có FOOD
        self.ghost_map = self.grid_2d.copy()
        # thay hết các FOOD trong ghost_map thành empty path
        self.ghost_map[self.ghost_map == FOOD] = ROAD

        # update pacman position in grid_2d
        # vị trí của PACMAN, FOOD, WALL
        self.grid_2d[pacman_i, pacman_j] = PACMAN
        self.grid_2d[self.grid_2d == GHOST] = ROAD

        # Vị trí bắt đầu vẽ map trong window

        self.start_y = start_y
        self.pacman_x, self.pacman_y = self.to_screen_coord(pacman_i, pacman_j)
        # self.start_x = start_x

        # self.score = 0
        self.font = pygame.font.Font(GAME_FONT, BLOCK_SIZE)

        self.pacman_block = None
        self.wall_blocks = pygame.sprite.Group()
        self.food_blocks = pygame.sprite.Group()
        self.ghost_blocks = pygame.sprite.Group()
        self.ghost_objs = []

        for i, row in enumerate(grid_2d): # không phải self.grid_2d
            for j, item in enumerate(row):
                x, y = self.to_screen_coord(i, j)
                if (x, y) == (self.pacman_x, self.pacman_y):
                    pacman_obj = pacman_graphic(self.pacman_x, self.pacman_y, height=BLOCK_SIZE, width=BLOCK_SIZE)
                    self.pacman_block = pacman_obj
                elif item == WALL:
                    wall_obj = wall_graphic(x, y, height=BLOCK_SIZE, width=BLOCK_SIZE)
                    self.wall_blocks.add(wall_obj)
                elif item == FOOD:
                    food_obj = food_graphic(x, y, height=BLOCK_SIZE, width=BLOCK_SIZE)
                    self.food_blocks.add(food_obj)
                elif item == GHOST:
                    ghost_obj = ghost_graphic(x, y, height=BLOCK_SIZE, width=BLOCK_SIZE)
                    self.ghost_objs.append(ghost_obj)
                    # self.ghost_blocks.append(pygame.sprite.GroupSingle(ghost_obj))
                    self.ghost_blocks.add(ghost_obj)


    def to_screen_coord(self, i: int, j: int) -> tuple:
        x = j * BLOCK_SIZE
        y = self.start_y + i * BLOCK_SIZE
        return x, y

    def to_cell_coord(self, x, y)->tuple:
        j = x // BLOCK_SIZE
        i = abs(y - self.start_y) // BLOCK_SIZE
        return i, j

    """
    Get the total size of the map
    return a pair (width, height)
    """
    @staticmethod
    def total_screen_size(grid_2d, start_y=0) -> tuple:

        ## Để ý trường hợp grid_2d is None
        n_rows = len(grid_2d)
        n_cols = len(grid_2d[0])
        height = BLOCK_SIZE * (n_rows) + start_y
        width = BLOCK_SIZE * (n_cols)
        return width, height

    def get_total_screen_size(self)->tuple:
        return map_graphic.total_screen_size(self.grid_2d, self.start_y)

    def draw_map(self):
        self.screen.fill(ROAD_COLOR)

        # --- Draw the game here ---
        self.wall_blocks.draw(self.screen)
        self.food_blocks.draw(self.screen)
        self.ghost_blocks.draw(self.screen)

        self.screen.blit(self.pacman_block.image, self.pacman_block.rect)

        # Render the text for the score
        score = self.pacman_block.score
        text = self.font.render("Score: " + str(score), True, Color.BLUE.value)

        # Put the text on the screen
        self.screen.blit(text, (0,0))

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def __str__(self):
        return_str = f"Screen size: {self.get_total_screen_size()}\n"\
                    f"Map size: {self.grid_2d.size}\n"\
                    f"Game over: {self.game_over}\n"
        return_str += "MAP:\n"
        return_str += ''.join(np.array2string(self.grid_2d, separator=',')) + "\n"
        return_str += "GHOST: \n"
        return_str += ''.join(np.array2string(self.ghost_map, separator=',')) + "\n"
        return return_str


class character_animation():

    """
    animaiton_img: một tấm ảnh biểu diễn animation
                    Kích thước tấm ảnh sẽ là (n * height, n * width) với n là số tấm ảnh con sẽ cắt ra để biểu diễn animation
    (height, width): chiều dài gốc của một tấm ảnh đơn
    """
    def __init__(self, animation_imgs, height, width):

        # một list object các hình khi chạy sẽ cho ra animation
        self.animations = [pygame.transform.scale(img, (width, height)) for img in animation_imgs]

        # Index đến tấm hình hiện tại trong self.animations
        self.clock = 0
        self.index = 0

    def get_current_image(self):
        return self.animations[self.index]

    def get_animation_list(self):
        return self.animations.copy()

    def get_animation_len(self):
        return len(self.animations)

    @DeprecationWarning
    @staticmethod
    def to_animation_list(animation_img, height, width, colorkey=ROAD_COLOR)->str:
        animations = []
        if animation_img.get_height() >= animation_img.get_width():
            n_img = animation_img.get_height() // animation_img.get_width()
            full_height = height * n_img
            full_width = width
        else:
            n_img = animation_img.get_width() // animation_img.get_height()
            full_height = height
            full_width = width * n_img

        resize_animation_img = pygame.transform.scale(animation_img, (full_width, full_height))
        resize_animation_img.set_colorkey(colorkey)

        for y in range(0, full_height, height):
            for x in range(0, full_width, width):
                # blank image
                image = pygame.Surface((width, height)).convert_alpha()
                image.set_colorkey(colorkey)

                # Vẽ đè animation_img vào image
                image.blit(resize_animation_img, (0,0), (x, y, width, height))
                # image.set_colorkey((0,0,0))
                animations.append(image)
                # print(x, y, width, height)
        # print()
        return animations

    def update(self, fps):
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
        # print(self.index)


class pacman_graphic(pygame.sprite.Sprite):

    '''
    (init_x, init_x): tọa độ của pac-man khi mới bắt đầu game
    img_path: đường dẫn file ảnh pac-man
    color_key: ảnh nền đồ họa pac-man
    '''
    def __init__(self, init_x, init_y, width, height,
                img_path=PACMAN_IMG, animation_paths=PACMAN_ANIMATION, color_key=ROAD_COLOR):

        super().__init__()

        # Ảnh hiện tại
        img = pygame.image.load(img_path).convert_alpha()
        img.set_colorkey(color_key)
        self.image = pygame.transform.scale(img, (width, height))
        # self.image = pygame.image.load(img_path).convert()
        # self.image.set_colorkey(color_key)

        self.moving_direction = None # Direction.UP.value, Direction.DOWN.value,...
        self.moving_steps = 0

        # Ảnh gốc
        self.original_image = self.image

        # Rectangle object
        self.rect = self.image.get_rect()

        # position
        self.rect.topleft = (init_x, init_y)

        self.score = 0

        # walk animations objects
        animation_imgs = [pygame.image.load(path).convert_alpha() for path in animation_paths]
        for i in animation_imgs:
            i.set_colorkey(color_key)

        left_flipped = list(map(lambda img: pygame.transform.flip(img, True, False), animation_imgs))

        up_flipped = list(map(lambda img: pygame.transform.rotate(img, 90), animation_imgs))

        down_flipped = [pygame.transform.rotate(img, 180) for img in up_flipped]

        self.right_animation = character_animation(animation_imgs, height=BLOCK_SIZE, width=BLOCK_SIZE)
        self.left_animation = character_animation(left_flipped, height=BLOCK_SIZE, width=BLOCK_SIZE)
        self.up_animation = character_animation(up_flipped, height=BLOCK_SIZE, width=BLOCK_SIZE)
        self.down_animation = character_animation(down_flipped, height=BLOCK_SIZE, width=BLOCK_SIZE)

        self.prev_i = -1
        self.prev_j = -1


    def is_moving(self)->bool:
        return self.moving_direction is not None

    """
    Chuyển hướng pacman theo một direction mới
    """
    def turn(self, direction: Direction):
        self.moving_direction = direction
        self.moving_steps = 0


    def update(self, map_obj:map_graphic, step_cost=PACMAN_STEP_COST,
                step_len=STEP_LEN, update_fps=PACMAN_ANIMATION_SPEED):
        if self.moving_direction is None:
            return

        cur_x, cur_y = self.rect.x, self.rect.y

        # Khi mà pacman đang di chuyển
        if self.moving_direction is not None and self.moving_steps < BLOCK_SIZE:
            # Khi Object bắt đầu di chuyển qua ô khác, cập nhật lại 2d grid:
            # if self.moving_steps == 0:
            #     i, j = map_obj.to_cell_coord(cur_x, cur_y)
            #     map_obj.grid_2d[i][j] = ROAD

            # Update lại tọa độ tùy thuộc vào hướng di chuyển
            if self.moving_direction == Direction.LEFT.value:
                self.left_animation.update(update_fps)
                self.image = self.left_animation.get_current_image()
                cur_x -= step_len

            elif self.moving_direction == Direction.RIGHT.value:
                self.right_animation.update(update_fps)
                self.image = self.right_animation.get_current_image()
                cur_x += step_len

            elif self.moving_direction == Direction.UP.value:
                self.up_animation.update(update_fps)
                self.image = self.up_animation.get_current_image()
                cur_y -= step_len

            elif self.moving_direction == Direction.DOWN.value:
                self.down_animation.update(update_fps)
                self.image = self.down_animation.get_current_image()
                cur_y += step_len
            else:
                raise Exception("UNKNOWN DIRECTION VALUE")
            self.moving_steps += step_len
        else:

            # Nếu đã di chuyển đến ô đích
            if self.moving_direction is not None:
                self.score -= step_cost

                # Cập nhật vị trí pacman trên grid_2d
                i, j = map_obj.to_cell_coord(cur_x, cur_y)
                map_obj.grid_2d[i, j] = PACMAN
                if self.prev_i != -1 and self.prev_j != -1:
                    map_obj.grid_2d[self.prev_i, self.prev_j] = ROAD
                self.prev_i, self.prev_j = i, j

                nrow = map_obj.grid_2d.shape[0]
                print(f"PACMAN POS: coord ({i}, {j})\t | cell {i + j * nrow}")

            self.moving_steps = 0
            self.moving_direction = None

            # self.image = self.original_image
            return

        # Dừng di chuyển khi đụng tường
        for block in pygame.sprite.spritecollide(self, map_obj.wall_blocks, False):
            block_x, block_y = block.rect.x, block.rect.y
            new_x, new_y = self.rect.x, self.rect.y

            if block_x != self.rect.x:
                if block_x < self.rect.x:
                    new_x = block_x + BLOCK_SIZE
                else:
                    new_x = block_x - BLOCK_SIZE
            elif block_y != self.rect.y:
                if block_y < self.rect.y:
                    new_y = block_y + BLOCK_SIZE
                else:
                    new_y = block_y - BLOCK_SIZE

            self.rect.topleft = new_x, new_y
            # print(self.rect.x, self.rect.y)
            self.moving_direction = None
            self.moving_steps = 0
            return

        # tránh object lọt ra khỏi map
        max_width, max_height = map_obj.get_total_screen_size()
        if cur_x >= 0 and cur_x <= max_width - BLOCK_SIZE:
            self.rect.x = cur_x

        if cur_y >= 0 and cur_y <= max_height - BLOCK_SIZE:
            self.rect.y = cur_y

    """
    Trả về một Direction random & hợp lệ từ map hiện tại
    """
    def random_moves(self, map_obj: map_graphic)->Direction:
        if self.is_moving():
            return None

        x, y = self.rect.topleft
        i, j = map_obj.to_cell_coord(x, y)
        candidates = []

        if j > 0 and map_obj.grid_2d[i, j - 1] != WALL:
            candidates.append(Direction.LEFT.value)

        if j < len(map_obj.grid_2d[0]) - 1 and map_obj.grid_2d[i, j + 1] != WALL:
            candidates.append(Direction.RIGHT.value)

        if i > 0 and map_obj.grid_2d[i - 1, j] != WALL:
            candidates.append(Direction.UP.value)

        if i < len(map_obj.grid_2d[0]) - 1 and map_obj.grid_2d[i + 1, j] != WALL:
            candidates.append(Direction.DOWN.value)

        if len(candidates) == 0:
            return None

        move = random.choice(candidates)
        return move


class ghost_graphic(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img_path=GHOST_IMG, color_key=ROAD_COLOR):
        super().__init__()
        img = pygame.image.load(img_path).convert_alpha()
        img.set_colorkey(color_key)

        self.image = pygame.transform.scale(img, (width, height))
        # self.image.set_colorkey(color_key)

        self.moving_direction = None #Direction.UP.value
        self.moving_steps = 0

        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

        self.prev_i = -1
        self.prev_j = -1

    def is_moving(self)->bool:
        return self.moving_direction is not None

    """
    Chuyển hướng GHOST theo một direction mới
    """
    def turn(self, direction: Direction):
        self.moving_direction = direction
        self.moving_steps = 0


    def update(self, map_obj:map_graphic, step_len=STEP_LEN):

        if self.moving_direction is None:
            return

        cur_x, cur_y = self.rect.x, self.rect.y

        if self.moving_direction is not None and self.moving_steps < BLOCK_SIZE:
            # if self.moving_steps == 0:
            #     i, j = map_obj.to_cell_coord(cur_x, cur_y)
            #     map_obj.ghost_map[i][j] = ROAD

            if self.moving_direction == Direction.LEFT.value:
                cur_x -= step_len
            elif self.moving_direction == Direction.RIGHT.value:
                cur_x += step_len
            elif self.moving_direction == Direction.UP.value:
                cur_y -= step_len
            elif self.moving_direction == Direction.DOWN.value:
                cur_y += step_len
            if (cur_x, cur_y) != (self.rect.x, self.rect.y):
                self.moving_steps += step_len
        else:
            if self.moving_direction is not None:
                # Cập nhật vị trí pacman trên grid_2d
                i, j = map_obj.to_cell_coord(cur_x, cur_y)
                map_obj.ghost_map[i, j] = GHOST
                if self.prev_i != -1 and self.prev_j != -1:
                    map_obj.ghost_map[self.prev_i, self.prev_j] = ROAD
                self.prev_i, self.prev_j = i, j
                # print("GHOST POS: ", i, j)

            self.moving_steps = 0
            self.moving_direction = None
            return


        for block in pygame.sprite.spritecollide(self, map_obj.wall_blocks, False):
            block_x, block_y = block.rect.x, block.rect.y
            new_x, new_y = self.rect.x, self.rect.y

            if block_x != self.rect.x:
                if block_x < self.rect.x:
                    new_x = block_x + BLOCK_SIZE
                else:
                    new_x = block_x - BLOCK_SIZE
            elif block_y != self.rect.y:
                if block_y < self.rect.y:
                    new_y = block_y + BLOCK_SIZE
                else:
                    new_y = block_y - BLOCK_SIZE

            self.rect.topleft = new_x, new_y

            # print(self.rect.x, self.rect.y)
            self.moving_direction = None
            self.moving_steps = 0

            return

        max_width, max_height = map_obj.get_total_screen_size()
        if cur_x >= 0 and cur_x <= max_width - BLOCK_SIZE:
            self.rect.x = cur_x

        if cur_y >= 0 and cur_y <= max_height - BLOCK_SIZE:
            self.rect.y = cur_y

    def get_current_pos(self)->tuple:
        return self.rect.x, self.rect.y

    """
    Trả về một Direction random & hợp lệ từ map hiện tại
    Return None nếu không có bất kỳ move hợp lệ nào
    """
    def random_moves(self, map_obj: map_graphic)->Direction:
        if self.is_moving():
            return None
        x, y = self.rect.topleft
        i, j = map_obj.to_cell_coord(x, y)
        candidates = []
        if j > 0 and map_obj.ghost_map[i, j - 1] != WALL:
            candidates.append(Direction.LEFT.value)

        if j < len(map_obj.ghost_map[0]) - 1 and map_obj.ghost_map[i, j + 1] != WALL:
            candidates.append(Direction.RIGHT.value)

        if i > 0 and map_obj.ghost_map[i - 1, j] != WALL:
            candidates.append(Direction.UP.value)

        if i < len(map_obj.ghost_map[0]) - 1 and map_obj.ghost_map[i + 1, j] != WALL:
            candidates.append(Direction.DOWN.value)

        if len(candidates) == 0:
            return None

        move = random.choice(candidates)
        # print("GHOST move to ", move)
        return move

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
        pygame.draw.ellipse(self.image, colorkey,(int(center/2), int(center/2), DOT_SIZE, DOT_SIZE))

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
