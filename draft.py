import pygame
import random
import math
from pygame import mixer
pygame.init()
pygame.font.init()


# create screen
clock = pygame.time.Clock()
width, height = 800, 600
surface = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load('C:\Dev\space invaders/bg.png')
background = pygame.transform.scale(background, (width, height))

# Backgrouund Sound
# mixer.music.load('background.wav')
# mixer.music.play(-1)


#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('C:\Dev\space invaders/player.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('C:\Dev\space invaders/ufo.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
player_vel = 5


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_vel = []
enemyY_vel = []
num_of_enemies = 6


for i in range(num_of_enemies):

    enemyImg.append(pygame.image.load('C:\Dev\space invaders/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_vel.append(4)
    enemyY_vel.append(.4)

# Bullet
bulletImg = pygame.image.load('C:\Dev\space invaders/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    surface.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    surface.blit(over_text, (200, 250))


def player(x, y):
    surface.blit(playerImg, (x, y))


def enemy(x, y, i):
    surface.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    surface.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) +
                         (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    clock.tick(60)
    surface.fill((0, 0, 0))
    # background imagea
    surface.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #bullet_sound = mixer.Sound("laser.wav")
                # bullet_sound.play()
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and playerX > 0:
        playerX -= player_vel
    if keys[pygame.K_d] and playerX < width - 60:
        playerX += player_vel

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > playerY:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_vel[i]
        enemyY[i] += enemyY_vel[i]
        if enemyX[i] <= 0:
            enemyX_vel[i] = 2
        elif enemyX[i] >= 740:
            enemyX_vel[i] = -2

    # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            #explosion_sound = mixer.Sound("explosion.wav")
            # explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

pygame.quit()
