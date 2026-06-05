import sys
import pygame
from Chess import ChessMain2

pygame.init()

screen_width = 512
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((255, 204, 153))

start_menu_image = pygame.image.load("images/menu-sprite.png")
pygame.display.set_caption('enjoy Alireza chess game project :)')
font = pygame.font.SysFont("Arial", 24, True, False)
input_box1 = pygame.Rect(screen_width/2 + 5, screen_height/2 - 150, 200, 50)
input_box2 = pygame.Rect(screen_width/2 + 5, screen_height/2 - 90, 200, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color1 = color_inactive
color2 = color_inactive
active1 = False
active2 = False
text1 = ''
text2 = ''
label1 = font.render("W", True, (255, 255, 255))
label2 = font.render("B", True, (0, 0, 0))
label_pos1 = (input_box1.x + input_box1.width + 10, input_box1.y + 9)
label_pos2 = (input_box2.x + input_box2.width + 10, input_box2.y + 9)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            ChessMain2.main(text1, text2)
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box1.collidepoint(event.pos):
                active1 = True
                active2 = False
            elif input_box2.collidepoint(event.pos):
                active1 = False
                active2 = True
            else:
                active1 = False
                active2 = False
            color1 = color_active if active1 else color_inactive
            color2 = color_active if active2 else color_inactive
        elif event.type == pygame.KEYDOWN:
            if active1:
                if event.key == pygame.K_BACKSPACE:
                    text1 = text1[:-1]
                    screen.fill((255, 204, 153))
                else:
                    text1 += event.unicode
            elif active2:
                if event.key == pygame.K_BACKSPACE:
                    text2 = text2[:-1]
                    screen.fill((255, 204, 153))
                else:
                    text2 += event.unicode

    screen.blit(start_menu_image, (0, 0))
    pygame.draw.rect(screen, color1, input_box1, 2)
    pygame.draw.rect(screen, color2, input_box2, 2)
    input_text1 = font.render(text1, True, (255, 0, 0))
    input_text2 = font.render(text2, True, (255, 0, 0))
    screen.blit(label1, label_pos1)
    screen.blit(label2, label_pos2)
    screen.blit(input_text1, (input_box1.x + 5, input_box1.y + 5))
    screen.blit(input_text2, (input_box2.x + 5, input_box2.y + 5))

    start_text = font.render("Enter player names and press Enter to start the game", True, (0, 0, 0))
    screen.blit(start_text, (screen_width / 2 - start_text.get_width() / 2, screen_height / 2 + 100))

    pygame.display.update()