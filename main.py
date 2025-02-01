from buttons import *
import pygame_gui

# pygame setup
pygame.init()
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
road_img = pygame.image.load("road.png")

logo_scale = 0.3
logo_img = pygame.image.load("logo.png")
logo_img = pygame.transform.scale(logo_img, (logo_img.get_width() * logo_scale, logo_img.get_height() * logo_scale))

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("gray")
    pygame.draw.rect(screen, "lime", (round(SCREEN_WIDTH/16), round(3 * SCREEN_HEIGHT/32), round(7 * SCREEN_WIDTH / 8), round(7 * SCREEN_HEIGHT / 8)))
    
    screen.blit(logo_img, (0, 0))

    # Update Écran
    pygame.display.flip()

    # FPS CAPPING (60)
    dt = clock.tick(60) / 1000

pygame.quit()