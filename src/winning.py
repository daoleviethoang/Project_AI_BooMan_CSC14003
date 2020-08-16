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

BACKGROUND_COLOR = (38, 44, 58)

font = pygame.font.Font(r'res/font.ttf', 25)
font2 = pygame.font.Font(r'res/font2.ttf', 63)
font3 = pygame.font.Font(r'res/font3.ttf', 40)
font4 = pygame.font.Font(r'res/font4.ttf', 110)
font5 = pygame.font.Font(r'res/font4.ttf', 50)
font6 = pygame.font.Font(r'res/font4.ttf', 25)
font7 = pygame.font.Font(r'res/font4.ttf', 34)
font8 = pygame.font.Font(r'res/font4.ttf', 83)

image2 = pygame.image.load(r'res/background2.png')
trophy = pygame.image.load(r'res/award.png')

def draw_Text(text, font, color, surface, x, y):
    textobj  = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (SCREEN_WIDTH//2, y)
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
    textrect.center = ((buttonx+(buttonwidth//2)), buttony+(buttonheight//2))
    surface.blit(textobj, textrect)

def text_inac(text, font, rect_text, inactive_color, active_color):
    cur = pygame.mouse.get_pos()
    x, y = rect_text.center
    if rect_text.collidepoint(cur):
        draw_Text2(text, font, active_color, screen, x, y)
    else:
        draw_Text2(text, font, inactive_color, screen, x, y)

def button2(text, x, y, width, height, inactive_color, active_color):
    cur = pygame.mouse.get_pos()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        text_to_button(text, font7, FONT_MENU_COLOR, screen, x, y, width, height)
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
        text_to_button(text, font7, FONT_MENU_COLOR, screen, x, y, width, height)


def winning_screen(flag, score, time):
    i = 0

    if flag == 2:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('res/end3.ogg'))
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('res/end1.ogg'), -1)
    else:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('res/end2.ogg'), -1)



    while True:
        screen.fill((0, 0, 0))
        screen.blit(image2, (0,0))      
                
        mx, my = pygame.mouse.get_pos()
        
        if flag == -1:
            draw_Text("Game got crashed by USER", font5, FONT_MENU_COLOR, screen, None, 290)
        
        elif flag == 0:
            stripe1 = pygame.Rect((SCREEN_WIDTH - 135)//2, 180, 3, 120)
            pygame.draw.rect(screen, FONT_MENU_COLOR, stripe1)
            stripe2 = pygame.Rect((SCREEN_WIDTH + 135)//2, 130, 3, 120)
            pygame.draw.rect(screen, FONT_MENU_COLOR, stripe2)

            draw_Text("SCORE", font5, FONT_MENU_COLOR, screen, None, 150)
                    
            draw_Text(str(i), font4, FONT_MENU_COLOR, screen, None, 230)
            if i != score:
                i += 1
            else: draw_Text("Time: "+ str(time) +"s", font6, FONT_MENU_COLOR, screen, None, 290)

            outline = pygame.Rect((SCREEN_WIDTH - 602 )//2, 349, 602, 52)
            pygame.draw.rect(screen, FONT_MENU_COLOR, outline)
            quote = pygame.Rect((SCREEN_WIDTH - 600 )//2, 350, 600, 50)
            pygame.draw.rect(screen, BACKGROUND_COLOR, quote)
            button2("Due to energy saver, it’s better not to move", (SCREEN_WIDTH - 600 )//2, 350, 600, 50, BACKGROUND_COLOR, BACKGROUND_COLOR)

        else:

            stripe1 = pygame.Rect(110, 180, 3, 120)
            pygame.draw.rect(screen, FONT_MENU_COLOR, stripe1)
            stripe2 = pygame.Rect(250, 130, 3, 120)
            pygame.draw.rect(screen, FONT_MENU_COLOR, stripe2)    

            draw_Text2("SCORE", font5, FONT_MENU_COLOR, screen, 180, 150)
            draw_Text2(str(i), font4, FONT_MENU_COLOR, screen, 180, 230)
            if i != score:
                i += 1
            else: 
                draw_Text2("Time: "+ str(time) +"s", font6, FONT_MENU_COLOR, screen, 180, 290)

                if flag == 1:
                    draw_Text2("GAME OVER", font8, FONT_MENU_COLOR, screen, 600, 220)
                    outline = pygame.Rect((SCREEN_WIDTH - 502 )//2, 370, 502, 52)
                    pygame.draw.rect(screen, FONT_MENU_COLOR, outline)
                    quote = pygame.Rect((SCREEN_WIDTH - 500 )//2, 371, 500, 50)
                    pygame.draw.rect(screen, BACKGROUND_COLOR, quote)
                    button2("Oh no.... Monster catched the pacman", (SCREEN_WIDTH - 500 )//2, 371, 500, 50, BACKGROUND_COLOR, BACKGROUND_COLOR)
                elif flag == 2:

                    screen.blit(trophy, (575, 230))

                    draw_Text2("VICTORY", font8, FONT_MENU_COLOR, screen, 600, 180)

                    outline = pygame.Rect((SCREEN_WIDTH - 442 )//2, 370, 442, 52)
                    pygame.draw.rect(screen, FONT_MENU_COLOR, outline)
                    quote = pygame.Rect((SCREEN_WIDTH - 440 )//2, 371, 440, 50)
                    pygame.draw.rect(screen, BACKGROUND_COLOR, quote)
                    button2("Pacman eats all the food!!!!!", (SCREEN_WIDTH - 440 )//2, 371, 440, 50, BACKGROUND_COLOR, BACKGROUND_COLOR)


        draw_Text("Do you want to continue?", font6, FONT_MENU_COLOR, screen, None, 470)
        rect1 = draw_Text2("MAIN MENU", font6, FONT2_MENU_COLOR, screen, 390, 515)
        # rect2 = draw_Text2("EXIT", font6, FONT2_MENU_COLOR, screen, 515, 515)
        underline1 = pygame.Rect(355, 530, 70, 3)
        pygame.draw.rect(screen, FONT2_MENU_COLOR, underline1)
        # underline2 = pygame.Rect(505, 530, 20, 3)
        # pygame.draw.rect(screen, FONT2_MENU_COLOR, underline2)

        if rect1.collidepoint((mx, my)):
            text_inac("MAIN MENU", font6, rect1, FONT2_MENU_COLOR, FONT_MENU_COLOR)
            if rect1.collidepoint((mx, my)):
                pygame.draw.rect(screen, FONT_MENU_COLOR, underline1)
            else: pygame.draw.rect(screen, FONT2_MENU_COLOR, underline1)
           
            if click:
                pass

        # if rect2.collidepoint((mx, my)):
        #     text_inac("EXIT", font6, rect2, FONT2_MENU_COLOR, FONT_MENU_COLOR)
        #     if rect2.collidepoint((mx, my)):
        #         pygame.draw.rect(screen, FONT_MENU_COLOR, underline2)
        #     else: pygame.draw.rect(screen, FONT2_MENU_COLOR, underline2)

            if click:
                pygame.quit()
                sys.exit()    

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
        mainClock.tick(40)
        
if __name__ == "__main__":
    winning_screen(1, 40, 125)
