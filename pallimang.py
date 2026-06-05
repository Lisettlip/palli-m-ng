import pygame  # Impordime pygame teegi
import sys  # Impordime sys teegi programmi sulgemiseks
import random  # Impordime random teegi juhuslikkuse jaoks

pygame.init()  # Käivitame pygame'i

width = 640  # Määrame ekraani laiuse
height = 480  # Määrame ekraani kõrguse

screen = pygame.display.set_mode((width, height))  # Loome mänguakna
pygame.display.set_caption("Ping Pong")  # Määrame akna pealkirja

bg = (220, 240, 255)  # Määrame taustavärvi
black = (0, 0, 0)  # Määrame musta värvi

ball_img = pygame.image.load("ball.png")  # Laeme palli pildi
pad_img = pygame.image.load("pad.png")  # Laeme aluse pildi

font = pygame.font.SysFont(None, 36)  # Loome fondi teksti jaoks
clock = pygame.time.Clock()  # Loome mängu kella

ball_size = 20  # Määrame palli suuruse
pad_width = 120  # Määrame aluse laiuse
pad_height = 20  # Määrame aluse kõrguse
pad_y = height / 1.5  # Määrame aluse kõrguse ekraanil
pad_speed = 4  # Määrame aluse liikumiskiiruse
moving_right = True  # Määrame, et alus alustab liikumist paremale


def reset_ball():  # Loome funktsiooni palli uuesti alustamiseks
    ball_x = random.randint(50, width - ball_size - 50)  # Valime pallile juhusliku x-asukoha
    ball_y = random.randint(50, 200)  # Valime pallile juhusliku y-asukoha
    ball_speed_x = random.choice([-4, 4])  # Valime pallile juhusliku vasakule või paremale suuna
    ball_speed_y = random.randint(3, 6)  # Valime pallile juhusliku alla liikumise kiiruse
    return ball_x, ball_y, ball_speed_x, ball_speed_y  # Tagastame palli andmed


def reset_game():  # Loome funktsiooni mängu algseisu jaoks
    ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()  # Taastame palli algseisu
    pad_x = 260  # Määrame aluse algse x-asukoha
    score = 0  # Määrame algskoori
    return ball_x, ball_y, ball_speed_x, ball_speed_y, pad_x, score  # Tagastame mängu andmed


ball_x, ball_y, ball_speed_x, ball_speed_y, pad_x, score = reset_game()  # Võtame mängu algväärtused

running = True  # Määrame, et mäng töötab
game_over = False  # Määrame, et mäng ei ole alguses läbi

while running:  # Peamine mängutsükkel

    for event in pygame.event.get():  # Kontrollime kõiki sündmuseid

        if event.type == pygame.QUIT:  # Kui kasutaja sulgeb akna
            pygame.quit()  # Sulgeme pygame'i
            sys.exit()  # Lõpetame programmi

        if game_over and event.type == pygame.KEYDOWN:  # Kui mäng on läbi ja vajutatakse klahvi
            if event.key == pygame.K_r:  # Kui vajutatakse R-klahvi
                ball_x, ball_y, ball_speed_x, ball_speed_y, pad_x, score = reset_game()  # Taastame mängu
                moving_right = True  # Paneme aluse jälle paremale liikuma
                game_over = False  # Mäng ei ole enam läbi

    if not game_over:  # Kui mäng ei ole läbi

        if moving_right:  # Kui alus liigub paremale
            pad_x += pad_speed  # Liigutame alust paremale

            if pad_x >= width - pad_width:  # Kui alus jõuab paremasse serva
                pad_x = width - pad_width  # Paneme aluse täpselt paremasse serva
                moving_right = False  # Muudame suuna vasakule

        else:  # Kui alus liigub vasakule
            pad_x -= pad_speed  # Liigutame alust vasakule

            if pad_x <= 0:  # Kui alus jõuab vasakusse serva
                pad_x = 0  # Paneme aluse täpselt vasakusse serva
                moving_right = True  # Muudame suuna paremale

        ball_x += ball_speed_x  # Liigutame palli x-suunas
        ball_y += ball_speed_y  # Liigutame palli y-suunas

        if ball_x <= 0 or ball_x >= width - ball_size:  # Kui pall puudutab külgseina
            ball_speed_x *= -1  # Muudame palli x-suuna vastupidiseks

        if ball_y <= 0:  # Kui pall puudutab ülemist seina
            ball_speed_y *= -1  # Muudame palli y-suuna vastupidiseks

        if ball_y >= height - ball_size:  # Kui pall kukub ekraani alla
            score -= 1  # Võtame ühe punkti maha
            ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()  # Paneme palli uuesti juhuslikust kohast tulema

        if (  # Kontrollime, kas pall põrkab aluse vastu
            ball_x + ball_size > pad_x and  # Kontrollime, kas palli parem serv on aluse vasakust servast paremal
            ball_x < pad_x + pad_width and  # Kontrollime, kas palli vasak serv on aluse paremast servast vasakul
            ball_y + ball_size > pad_y and  # Kontrollime, kas palli alumine serv on aluse ülemisest servast allpool
            ball_y < pad_y + pad_height and  # Kontrollime, kas palli ülemine serv on aluse alumisest servast ülevalpool
            ball_speed_y > 0  # Kontrollime, kas pall liigub alla
        ):  # Kui kõik tingimused on tõesed
            ball_speed_y *= -1  # Paneme palli üles põrkama
            score += 1  # Lisame ühe punkti

        screen.fill(bg)  # Värvime tausta

        screen.blit(  # Joonistame palli
            pygame.transform.scale(ball_img, (ball_size, ball_size)),  # Muudame palli pildi suurust
            (ball_x, ball_y)  # Määrame palli asukoha
        )  # Lõpetame palli joonistamise

        screen.blit(  # Joonistame aluse
            pygame.transform.scale(pad_img, (pad_width, pad_height)),  # Muudame aluse pildi suurust
            (pad_x, pad_y)  # Määrame aluse asukoha
        )  # Lõpetame aluse joonistamise

        text = font.render(f"Punktid: {score}", True, black)  # Loome punktide teksti
        screen.blit(text, (20, 20))  # Kuvame punktid ekraanile

    pygame.display.update()  # Uuendame ekraani
    clock.tick(60)  # Hoiame mängu 60 kaadrit sekundis
