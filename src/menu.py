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
font = pygame.font.Font(r'font.ttf', 25)

image = pygame.image.load(r'background.png')


def draw_Text(text, font, color, surface, x, y):
    textobj  = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (SCREEN_WIDTH/2, y)
    surface.blit(textobj, textrect)

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
                game()
                pygame.mixer.music.play(-1) 
        if button_2.collidepoint((mx, my)):
            if click:
                options()
                pygame.mixer.music.play(-1)   
        if button_3.collidepoint((mx, my)):
            if click:
                options()
                pygame.mixer.music.play(-1)   
        if button_4.collidepoint((mx, my)):
            if click:
                options()
                pygame.mixer.music.play(-1)                    
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

def game():
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    draw_Text('GAME', font, (255, 255, 255), screen, 20, 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)

def options():
    pygame.mixer.music.stop()
    screen.fill((0, 0, 0))
    draw_Text('OPTIONS', font, (255, 255, 255), screen, 20, 20)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                

        pygame.display.update()
        mainClock.tick(60)


Main_Menu()
