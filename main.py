import pygame
pygame.init()

# Window global variables
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 900, 600
WIN = pygame.display.set_mode(WIN_SIZE)
FPS = 60

# Background
SPACE_IMG = pygame.transform.scale(pygame.image.load("Assets\space.png"),WIN_SIZE)

# Spaceship global variables
SPACESHIP_SIZE = SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60,50
SPACESHIP_VELOCITY = 5

# Yellow spaceship global variables
YELLOW_SPACESHIP_IMG = pygame.image.load("Assets\spaceship_yellow.png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG, SPACESHIP_SIZE), 90)
YELLOW_SPACESHIP_SPAWN_COORDINATES = YELLOW_SPACESHIP_SPAWN_X, YELLOW_SPACESHIP_SPAWN_Y = 80, (WIN_HEIGHT // 2 - YELLOW_SPACESHIP.get_height() // 2)
YELLOW_SPACESHIP_SHOOT_BIND = pygame.K_SPACE

# Red spaceship global variables
RED_SPACESHIP_IMAGE = pygame.image.load("Assets\spaceship_red.png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, SPACESHIP_SIZE), -90)
RED_SPACESHIP_SPAWN_COORDINATES = RED_SPACESHIP_SPAWN_X, RED_SPACESHIP_SPAWN_Y = WIN_WIDTH - 80 - (SPACESHIP_HEIGHT // 2), (WIN_HEIGHT // 2 - YELLOW_SPACESHIP.get_height() // 2)
RED_SPACESHIP_SHOOT_BIND = pygame.K_RCTRL
# Movement border
BORDER_WIDTH = 25
BORDER = pygame.Rect(WIN_WIDTH // 2 - (BORDER_WIDTH // 2), 0, BORDER_WIDTH, WIN_HEIGHT)

# Bullet global variables
BULLET_VELOCITY = 10
BULLET_THICKNESS = 5
BULLET_LENGTH = 20
MAX_ACTIVE_BULLETS = 3

EVENT_YELLOW_ISHIT = pygame.USEREVENT + 1
EVENT_RED_ISHIT = pygame.USEREVENT + 2

pygame.display.set_caption("First pygame game!")


def draw_window(P1, P2, yellow_bullets, red_bullets):
    WIN.blit(SPACE_IMG, (0,0))
    WIN.blit(YELLOW_SPACESHIP, (P1.x, P1.y))
    WIN.blit(RED_SPACESHIP, (P2.x, P2.y))
    pygame.draw.rect(WIN, (0,0,0), BORDER)
    for yellow_bullet in yellow_bullets:
        pygame.draw.rect(WIN, (255, 255, 0), yellow_bullet)
    for red_bullet in red_bullets:
        pygame.draw.rect(WIN, (255,0,0), red_bullet)
    
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

def handle_bullets(yellow_bullets: list, red_bullets: list, yellow: pygame.Rect, red: pygame.Rect):
    # Yellow bullets
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if bullet.x + BULLET_LENGTH > WIN_WIDTH:
            yellow_bullets.remove(bullet)
        elif red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(EVENT_RED_ISHIT))
        
    # Red bullets
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if bullet.x < 0:
            red_bullets.remove(bullet)
        elif yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(EVENT_YELLOW_ISHIT))
            


def main():
    yellow = pygame.Rect(YELLOW_SPACESHIP_SPAWN_COORDINATES, SPACESHIP_SIZE)
    red = pygame.Rect(RED_SPACESHIP_SPAWN_COORDINATES, SPACESHIP_SIZE)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == YELLOW_SPACESHIP_SHOOT_BIND and len(yellow_bullets) < MAX_ACTIVE_BULLETS: # Yellow shoot 
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - BULLET_THICKNESS//2, BULLET_LENGTH,  BULLET_THICKNESS)
                    yellow_bullets.append(bullet)

                if event.key == RED_SPACESHIP_SHOOT_BIND and len(red_bullets) < MAX_ACTIVE_BULLETS: # Red shoot
                    bullet = pygame.Rect(red.x - BULLET_LENGTH + red.width, red.y + red.height//2 - BULLET_THICKNESS//2, BULLET_LENGTH,  BULLET_THICKNESS)
                    red_bullets.append(bullet)

            if event.type == EVENT_YELLOW_ISHIT:
                yellow_health -= 1 # Reduce yellow player health

            if event.type == EVENT_RED_ISHIT:
                red_health -= 1 # Reduce red player health

        if yellow_health <= 0:
            winner_text = "Red wins!"
        if red_health <= 0:
            winner_text = "Yellow wins!"
            
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets)

if __name__ == "__main__":
    main()