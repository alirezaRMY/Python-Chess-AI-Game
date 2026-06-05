import pygame
import sys
from Chess import ChessMain3
pygame.init()

window_width = 512
window_height = 512

background_image = pygame.image.load("images/menu-sprite.png")

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("enjoy Alireza Ramyad's chess game project :)")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

button_width = 240
button_height = 50
button_1_pos = (300, 225)
button_2_pos = (265, 150)
button_3_pos = (265, 300)

button_font = pygame.font.SysFont("Arial", 25, True, False)

screen.fill((0, 0, 128))
screen.blit(background_image, (0, 0))

button_1 = pygame.draw.rect(screen, WHITE, (button_1_pos[0], button_1_pos[1], 200, button_height))
button_1_text = button_font.render("Play versus AI", True, BLACK)
button_1_text_rect = button_1_text.get_rect(center=button_1.center)
screen.blit(button_1_text, button_1_text_rect)

button_2 = pygame.draw.rect(screen, WHITE, (button_2_pos[0], button_2_pos[1], button_width, button_height))
button_2_text = button_font.render("Play versus your Friend", True, BLACK)
button_2_text_rect = button_2_text.get_rect(center=button_2.center)
screen.blit(button_2_text, button_2_text_rect)


button_3 = pygame.draw.rect(screen, WHITE, (button_3_pos[0], button_3_pos[1], button_width, button_height))
button_3_text = button_font.render("AI versus AI (tutorial)", True, BLACK)
button_3_text_rect = button_3_text.get_rect(center=button_3.center)
screen.blit(button_3_text, button_3_text_rect)

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_1.collidepoint(mouse_pos):
                exec(open("predisplay.py").read())
            elif button_2.collidepoint(mouse_pos):
                exec(open("predisplay2.py").read())
            elif button_3.collidepoint(mouse_pos):
                ChessMain3.main("White_AI")
