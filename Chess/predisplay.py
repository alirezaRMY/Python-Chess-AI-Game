import pygame
import sys
from Chess import ChessMain


pygame.init()

screen_width = 512
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((255, 204, 153))

start_menu_image = pygame.image.load("images/menu-sprite.png")
pygame.display.set_caption("enjoy Alireza(RM)'s chess game project :)")
font = pygame.font.SysFont("Arial", 25, True, False)
input_box = pygame.Rect(screen_width/2 - 30, screen_height/2 - 100, 200, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
label = font.render("W", True, (255, 255, 255))
label_pos = (input_box.x + input_box.width + 20, input_box.y + 13)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            ChessMain.main(text)
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    screen.fill((255, 204, 153))
                else:
                    text += event.unicode

    screen.blit(start_menu_image, (0, 0))
    pygame.draw.rect(screen, color, input_box, 2)
    input_text = font.render(text, True, (255, 0, 0))
    screen.blit(label, label_pos)
    screen.blit(input_text, (input_box.x + 5, input_box.y + 5))



    start_text = font.render("Enter your name and press Enter to start the game", True, (0, 0, 0))
    screen.blit(start_text, (screen_width / 2 - start_text.get_width() / 2, screen_height / 2 + 100))

    pygame.display.update()