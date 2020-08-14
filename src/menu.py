import pygame, sys

from pygame.locals import *

#Initialize pygame
pygame.init()
mainClock = pygame.time.Clock()
#create the screen 
pygame.display.set_caption('PACMAN')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

COLOR_MENU = (0, 102, 37)
COLOR2_MENU = (26, 255, 110)
EXIT_COLOR = (153, 0, 0)
EXIT2_COLOR = (255, 0, 0)
FONT_MENU_COLOR = (255, 255, 255)
FONT2_MENU_COLOR = (153, 153, 153)
FONT_MAP_COLOR = (115, 115, 115)
font = pygame.font.Font(r'font.ttf', 25)
font2 = pygame.font.Font(r'font2.ttf', 63)
font3 = pygame.font.Font(r'font3.ttf', 40)

image = pygame.image.load(r'background.png')


def draw_Text(text, font, color, surface, x, y):
    textobj  = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (SCREEN_WIDTH/2, y)
    surface.blit(textobj, textrect)

def draw_Text2(text, font, color, surface, x, y):
    textobj  = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect

def text_to_button(text, font, color, surface, buttonx, buttony, buttonwidth, buttonheight):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    surface.blit(textobj, textrect)

def button(text, x, y, width, height, inactive_color, active_color):
    cur = pygame.mouse.get_pos()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        text_to_button(text, font, FONT_MENU_COLOR, screen, x, y, width, height)
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
        text_to_button(text, font, FONT2_MENU_COLOR, screen, x, y, width, height)

def text_inac(text, rect_text, inactive_color, active_color):
    cur = pygame.mouse.get_pos()
    x, y = rect_text.center
    if rect_text.collidepoint(cur):
        draw_Text2(text, font3, active_color, screen, x, y)
    else:
        draw_Text2(text, font3, inactive_color, screen, x, y)

click = False


def Main_Menu():
    pygame.mixer.music.load('start.mp3')
    pygame.mixer.music.play(-1)  
    while True:
        screen.fill((0, 0, 0))
        screen.blit(image, (0,0))      
        
        
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect((SCREEN_WIDTH - 200 )/2, 220, 200, 50)
        button_2 = pygame.Rect((SCREEN_WIDTH - 200 )/2, 290, 200, 50)
        button_3 = pygame.Rect((SCREEN_WIDTH - 200 )/2, 360, 200, 50)
        button_4 = pygame.Rect((SCREEN_WIDTH - 200 )/2, 430, 200, 50)
        button_5 = pygame.Rect((SCREEN_WIDTH - 200 )/2, 500, 200, 50)


        if button_1.collidepoint((mx, my)):
            if click:
                choose_map('LEVEL1')
        
        if button_2.collidepoint((mx, my)):
            if click:
                choose_map('LEVEL2')
        if button_3.collidepoint((mx, my)):
            if click:
                choose_map('LEVEL3')
        if button_4.collidepoint((mx, my)):
            if click:
                choose_map('LEVEL4')
        if button_5.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()  

        pygame.draw.rect(screen, COLOR_MENU, button_1)
        button("LEVEL 1", (SCREEN_WIDTH - 200 )/2, 220, 200, 50, COLOR_MENU, COLOR2_MENU)
        pygame.draw.rect(screen, COLOR_MENU, button_2)
        button("LEVEL 2", (SCREEN_WIDTH - 200 )/2, 290, 200, 50, COLOR_MENU, COLOR2_MENU)
        pygame.draw.rect(screen, COLOR_MENU, button_3)
        button("LEVEL 3", (SCREEN_WIDTH - 200 )/2, 360, 200, 50, COLOR_MENU, COLOR2_MENU)
        pygame.draw.rect(screen, COLOR_MENU, button_4)
        button("LEVEL 4", (SCREEN_WIDTH - 200 )/2, 430, 200, 50, COLOR_MENU, COLOR2_MENU)
        pygame.draw.rect(screen, EXIT_COLOR, button_5)
        button("EXIT", (SCREEN_WIDTH - 200 )/2, 500, 200, 50, EXIT_COLOR, EXIT2_COLOR)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

def choose_map(level):
    screen.fill((0, 0, 0))
    screen.blit(image, (0,0))

    draw_Text(level, font2, (255, 255, 255), screen, 20, 110)

    running = True
    while running:
        mx, my = pygame.mouse.get_pos()

        button1 = pygame.Rect(540, 520, 175, 50)
        button2 = pygame.Rect(95, 520, 175, 50)        

        if button1.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        if button2.collidepoint((mx, my)):
            if click:
                running = False    
        
        pygame.draw.rect(screen, EXIT_COLOR, button1)
        button("EXIT", 540, 520, 175, 50, EXIT_COLOR, EXIT2_COLOR)
        pygame.draw.rect(screen, EXIT_COLOR, button2)
        button("BACK", 95, 520, 175, 50, EXIT_COLOR, EXIT2_COLOR)
        

        rect_text = []
        index = 1
        posx = 100
        for i in range(1, 6):
            posy = 223 
            for j in range(1, 6):
                rect_text.append(draw_Text2("Map " + str(index), font3, FONT_MAP_COLOR, screen, posx, posy))
                posy += 68
                index += 1
            posx += 150 

        for i in range (25):
            if rect_text[i].collidepoint((mx, my)):
                text_inac("Map "+ str(i+1), rect_text[i], FONT_MAP_COLOR, FONT_MENU_COLOR)                
                if click:
                    load_game("input/" + str(level[5]) + "/input" + str(i+1) + ".txt" ,level)


        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True            

        pygame.display.update()
        mainClock.tick(60)

def load_game(path, level):
    print(path)


Main_Menu()
