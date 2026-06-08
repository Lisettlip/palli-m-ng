import pygame  # Impordime pygame teegi
import sys  # Impordime sys teegi programmi sulgemiseks
import random  # Impordime random teegi juhuslikkuse jaoks

pygame.init()  # Käivitame pygame'i

pygame.mixer.music.load("856395__hermeshermeshermes__guitar-loop-1-emaj7dmaj7-112bpm.wav")  # Laeme taustamuusika
pygame.mixer.music.play(-1)  # Mängime taustamuusikat lõputult

jump_sound = pygame.mixer.Sound("Jump7.wav")  # Laeme palli põrkeheli

width = 640  # Määrame ekraani laiuse
height = 480  # Määrame ekraani kõrguse

screen = pygame.display.set_mode((width, height))  # Loome mänguakna
pygame.display.set_caption("Ping Pong")  # Määrame akna pealkirja

bg = (73, 151, 208)  # Määrame taustavärvi
black = (0, 0, 0)  # Määrame musta värvi

ball_img = pygame.image.load("ball.png")  # Laeme palli pildi
pad_img = pygame.image.load("pad.png")  # Laeme aluse pildi

font = pygame.font.SysFont(None, 36)  # Loome fondi teksti jaoks
clock = pygame.time.Clock()  # Loome mängu kella

ball_size = 20  # Määrame palli suuruse
pad_width = 120  # Määrame aluse laiuse
pad_height = 20  # Määrame aluse kõrguse
pad_y = height / 1.5  # Määrame aluse y-asukoha
pad_speed = 6  # Määrame aluse liikumiskiiruse


def reset_ball():  # Loome funktsiooni palli algseisu jaoks
    ball_x = random.randint(0, width - ball_size)  # Määrame pallile juhusliku x-asukoha
    ball_y = 0  # Pall alustab ülevalt
    ball_speed_x = random.choice([-3, 3])  # Määrame pallile juhusliku x-suuna
    ball_speed_y = random.randint(3, 6)  # Määrame pallile juhusliku y-kiiruse
    return ball_x, ball_y, ball_speed_x, ball_speed_y  # Tagastame palli andmed


def reset_game():  # Loome funktsiooni mängu uuesti alustamiseks
    ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()  # Taastame palli algseisu
    pad_x = 260  # Määrame aluse algse x-asukoha
    score = 0  # Määrame punktid nulli
    return ball_x, ball_y, ball_speed_x, ball_speed_y, pad_x, score  # Tagastame mängu andmed


ball_x, ball_y, ball_speed_x, ball_speed_y, pad_x, score = reset_game()  # Määrame mängu algväärtused

running = True  # Määrame, et mäng töötab
game_over = False  # Määrame, et mäng ei ole alguses läbi

while running:  # Peamine mängutsükkel

    for event in pygame.event.get():  # Kontrollime kõiki sündmusi

        if event.type == pygame.QUIT:  # Kui kasutaja sulgeb akna
            pygame.quit()  # Sulgeme pygame'i
            sys.exit()  # Lõpetame programmi

        if game_over and event.type == pygame.KEYDOWN:  # Kui mäng on läbi ja vajutatakse klahvi
            if event.key == pygame.K_r:  # Kui vajutatakse R-klahvi
                ball_x, ball_y, ball_speed_x, ball_speed_y, pad_x, score = reset_game()  # Taastame mängu
                game_over = False  # Mäng ei ole enam läbi

    if not game_over:  # Kui mäng ei ole läbi

        keys = pygame.key.get_pressed()  # Loeme klaviatuuri olekut

        if keys[pygame.K_LEFT]:  # Kui vajutatakse vasakut noolt
            pad_x -= pad_speed  # Liigutame alust vasakule

        if keys[pygame.K_RIGHT]:  # Kui vajutatakse paremat noolt
            pad_x += pad_speed  # Liigutame alust paremale

        if pad_x < 0:  # Kui alus läheb vasakust servast välja
            pad_x = 0  # Paneme aluse tagasi vasakusse serva

        if pad_x > width - pad_width:  # Kui alus läheb paremast servast välja
            pad_x = width - pad_width  # Paneme aluse tagasi paremasse serva

        ball_x += ball_speed_x  # Liigutame palli x-suunas
        ball_y += ball_speed_y  # Liigutame palli y-suunas

        if ball_x <= 0 or ball_x >= width - ball_size:  # Kui pall puudutab külgseina
            ball_speed_x *= -1  # Muudame palli x-suuna vastupidiseks

        if ball_y <= 0:  # Kui pall puudutab ülemist serva
            ball_speed_y *= -1  # Muudame palli y-suuna vastupidiseks

        if ball_y >= height - ball_size:  # Kui pall puudutab alumist serva
            game_over = True  # Mäng lõppeb

        if (  # Kontrollime, kas pall puudutab alust
            ball_x + ball_size > pad_x and  # Palli parem serv on aluse vasakust servast paremal
            ball_x < pad_x + pad_width and  # Palli vasak serv on aluse paremast servast vasakul
            ball_y + ball_size > pad_y and  # Palli alumine serv on aluse ülemisest servast allpool
            ball_y < pad_y + pad_height and  # Palli ülemine serv on aluse alumisest servast ülevalpool
            ball_speed_y > 0  # Pall liigub alla
        ):  # Kui kõik tingimused on täidetud
            ball_speed_y *= -1  # Pall põrkab üles
            score += 1  # Lisame ühe punkti
            jump_sound.play()  # Mängime heli ainult aluse puudutamisel

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

    if game_over:  # Kui mäng on läbi
        text1 = font.render("MÄNG ON LÄBII!", True, black)  # Loome mängu lõpu teksti
        text2 = font.render("Vajuta R, et uuesti alustada", True, black)  # Loome uuesti alustamise juhise

        screen.blit(text1, (220, 200))  # Kuvame mängu lõpu teksti
        screen.blit(text2, (140, 250))  # Kuvame juhise ekraanile

    pygame.display.update()  # Uuendame ekraani
    clock.tick(60)  # Hoiame mängu 60 kaadrit sekundis