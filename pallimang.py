import pygame
import sys

pygame.init()

# Ekraani suurus
width = 640
height = 480

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

# Värvid
bg = (220, 240, 255)
black = (0, 0, 0)

# Pildid
ball_img = pygame.image.load("ball.png")
pad_img = pygame.image.load("pad.png")

# Font
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()


# Funktsioon mängu algseisu jaoks
def reset_game():
    ball_x = 320
    ball_y = 240
    ball_speed_x = 4
    ball_speed_y = 3

    pad_x = 260

    score = 0

    return ball_x, ball_y, ball_speed_x, ball_speed_y, pad_x, score


# Algväärtused
ball_size = 20

pad_width = 120
pad_height = 20
pad_y = height / 1.5
pad_speed = 6

ball_x, ball_y, ball_speed_x, ball_speed_y, pad_x, score = reset_game()

running = True
game_over = False

while running:

    # Eventid
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Restart R-klahviga
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:

                ball_x, ball_y, ball_speed_x, ball_speed_y, pad_x, score = reset_game()

                game_over = False

    # Kui mäng käib
    if not game_over:

        # Klaviatuur
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            pad_x -= pad_speed

        if keys[pygame.K_RIGHT]:
            pad_x += pad_speed

        # Piirid
        if pad_x < 0:
            pad_x = 0

        if pad_x > width - pad_width:
            pad_x = width - pad_width

        # Palli liikumine
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Seinad
        if ball_x <= 0 or ball_x >= width - ball_size:
            ball_speed_x *= -1

        if ball_y <= 0:
            ball_speed_y *= -1

        # Pall kukub alla
        if ball_y >= height - ball_size:
            game_over = True

        # Kokkupõrge alusega
        if (
            ball_x + ball_size > pad_x and
            ball_x < pad_x + pad_width and
            ball_y + ball_size > pad_y and
            ball_y < pad_y + pad_height and
            ball_speed_y > 0
        ):
            ball_speed_y *= -1
            score += 1

        # Taust
        screen.fill(bg)

        # Pall
        screen.blit(
            pygame.transform.scale(ball_img, (ball_size, ball_size)),
            (ball_x, ball_y)
        )

        # Alus
        screen.blit(
            pygame.transform.scale(pad_img, (pad_width, pad_height)),
            (pad_x, pad_y)
        )

        # Punktid
        text = font.render(f"Punktid: {score}", True, black)
        screen.blit(text, (20, 20))

    # GAME OVER
    else:

        screen.fill(bg)

        game_text = font.render("GAME OVER", True, black)
        screen.blit(game_text, (220, 180))

        score_text = font.render(f"Skoor: {score}", True, black)
        screen.blit(score_text, (250, 230))

        restart_text = font.render("Vajuta R, et uuesti alustada", True, black)
        screen.blit(restart_text, (120, 300))

    pygame.display.update()
    clock.tick(60)