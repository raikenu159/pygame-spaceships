import pygame
pygame.init()

# Window global variables
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 900, 600
WIN = pygame.display.set_mode(WIN_SIZE)
FPS = 60

# Spaceship global variables
SPACESHIP_SIZE = SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60,50
SPACESHIP_VELOCITY = 5

# Yellow spaceship global variables
YELLOW_SPACESHIP_IMAGE = pygame.image.load("Assets\spaceship_yellow.png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, SPACESHIP_SIZE), 90)
YELLOW_SPACESHIP_SPAWN_COORDINATES = YELLOW_SPACESHIP_SPAWN_X, YELLOW_SPACESHIP_SPAWN_Y = 80, (WIN_HEIGHT / 2 - YELLOW_SPACESHIP.get_height() / 2)

# Red spaceship global variables
RED_SPACESHIP_IMAGE = pygame.image.load("Assets\spaceship_red.png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, SPACESHIP_SIZE), -90)
RED_SPACESHIP_SPAWN_COORDINATES = RED_SPACESHIP_SPAWN_X, RED_SPACESHIP_SPAWN_Y = WIN_WIDTH - 80 - (SPACESHIP_HEIGHT / 2), (WIN_HEIGHT / 2 - YELLOW_SPACESHIP.get_height() / 2)

# Movement border
BORDER_WIDTH = 25
BORDER = pygame.Rect(WIN_WIDTH / 2 - (BORDER_WIDTH / 2), 0, BORDER_WIDTH, WIN_HEIGHT)

# Bullet global variables
BULLET_VELOCITY = 7

pygame.display.set_caption("First pygame game!")


def draw_window(P1, P2):
    WIN.fill((50,50,50))
    WIN.blit(YELLOW_SPACESHIP, (P1.x, P1.y))
    WIN.blit(RED_SPACESHIP, (P2.x, P2.y))
    pygame.draw.rect(WIN, (0,0,0), BORDER)
    pygame.display.update()

def yellow_handle_movement(keys, yellow): # Yellow spaceship movement
        if keys[pygame.K_a] and yellow.x - SPACESHIP_VELOCITY > 0: # LEFT
            yellow.x -= SPACESHIP_VELOCITY
        if keys[pygame.K_d] and yellow.x + SPACESHIP_HEIGHT + SPACESHIP_VELOCITY < BORDER.x: # RIGHT 
            yellow.x += SPACESHIP_VELOCITY
        if keys[pygame.K_w] and yellow.y > 0: # UP
            yellow.y -= SPACESHIP_VELOCITY
        if keys[pygame.K_s] and yellow.y + SPACESHIP_VELOCITY < WIN_HEIGHT - SPACESHIP_HEIGHT: # DOWN
            yellow.y += SPACESHIP_VELOCITY
def red_handle_movement(keys, red): # Red spaceship movement
        # Red spaceship movement
        if keys[pygame.K_KP4] and red.x - SPACESHIP_VELOCITY > BORDER.x + BORDER.width: # LEFT
            red.x -= SPACESHIP_VELOCITY
        if keys[pygame.K_KP6] and red.x + SPACESHIP_VELOCITY < WIN_WIDTH - SPACESHIP_HEIGHT: # RIGHT 
            red.x += SPACESHIP_VELOCITY
        if keys[pygame.K_KP8] and red.y > 0: # UP
            red.y -= SPACESHIP_VELOCITY
        if keys[pygame.K_KP5] and red.y + SPACESHIP_VELOCITY < WIN_HEIGHT - SPACESHIP_HEIGHT: # DOWN
            red.y += SPACESHIP_VELOCITY

def main():
    yellow = pygame.Rect(YELLOW_SPACESHIP_SPAWN_COORDINATES, SPACESHIP_SIZE)
    red = pygame.Rect(RED_SPACESHIP_SPAWN_COORDINATES, SPACESHIP_SIZE)

    bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        draw_window(yellow, red)

if __name__ == "__main__":
    main()