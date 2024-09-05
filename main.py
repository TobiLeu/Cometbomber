import sys

import pygame
import random
from sys import exit

# Initialisiere Pygame
pygame.init()
pygame.mixer.init()

# Spielkonstanten
SCREEN_HEIGHT = 720
GAME_SCREEN_WIDTH = 1160
GAME_SCREEN_HEIGHT = 680
TILE_SIZE = 40
PLAYER_SPEED = 3
ENEMY_SPEED = 1
PLAYER_SIZE = 30
BOMB_TIME = 3000  # Zeit bis zur Explosion in Millisekunden
EXPLOSION_DURATION = 1500  # Dauer der Explosion in Millisekunden
PLAYER_START_POSITION = 1  # Startposition des Spielers
PLAYER_BOMB_MAXIMUM = 3
GRANIT_POSITIONS = [32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58,
                    92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118,
                    152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178,
                    212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238,
                    272, 274, 276, 278, 280, 282, 284, 286, 288, 290, 292, 294, 296, 298,
                    332, 334, 336, 338, 340, 342, 344, 346, 348, 350, 352, 354, 356, 358,
                    392, 394, 396, 398, 400, 402, 404, 406, 408, 410, 412, 414, 416, 418,
                    452, 454, 456, 458, 460, 462, 464, 466, 468, 470, 472, 474, 476, 478]  # Granit = nicht zerstörbares Hindernis

STONE_POSITIONS = [3,4,5,10,16,22,28,29,
                   43,59,
                   63,67,69,75,76,79,85,
                   91,109,113,
                   121,125,126,134,139,142,134,146,
                   151,153,155,163,177,
                   186,190,191,196,197,204,
                   213,239,
                   244,249,250,255,256,259,260,262,266,
                   271,295,297,
                   304,314,316,324,
                   335,341,343,349,355,
                   366,372,373,377,378,379,382,383,
                   397,413,
                   429,432,436,439,448,449,
                   451,471,
                   482,486,492,496,501,502,506,507,508] # = zerstörbares Hindernis
SCORE_VALUE_STONE = 10
PLAYER_SCORE = 0
ENEMY_POSITIONS = [131,265]
ENEMY_DIRECTION_CHANGE_INTERVAL = 5000  # Zeit in Millisekunden
GAME_DURATION = 180000  # Spieldauer in Millisekunden (z. B. 120000 ms = 2 Minuten)

start_time = pygame.time.get_ticks()  # Startzeit des Spiels

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (90, 90, 90)
BACKGROUND = (244, 164, 96)

# Schriftarten laden
title_font = pygame.font.SysFont('Impact', 72)
instruction_font = pygame.font.SysFont('Impact', 36)
infobar_font = pygame.font.SysFont('Impact', 20)

# Bildschirm einrichten
screen = pygame.display.set_mode((GAME_SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cometbomber")

# Spieluhr
clock = pygame.time.Clock()

# Funktionen Spielfeld in Rastereinteilung: x-Koordinate, y-Koordinate
def player_x_position(pos_number):
    if (pos_number % 30) == 0:
        x_coordinate = (pos_number % 30) * TILE_SIZE + GAME_SCREEN_WIDTH - TILE_SIZE
    else:
        x_coordinate = (pos_number % 30) * TILE_SIZE - TILE_SIZE
    return x_coordinate
def player_y_position(pos_number):
    if (pos_number % 30) == 0:
        y_coordinate = (int(pos_number / 30)) * TILE_SIZE - TILE_SIZE
    else:
        y_coordinate = (int(pos_number / 30)) * TILE_SIZE
    return y_coordinate
def x_position(pos_number):
    if (pos_number % 30) == 0:
        x_coordinate = (pos_number % 30) * TILE_SIZE + GAME_SCREEN_WIDTH - TILE_SIZE
    else:
        x_coordinate = (pos_number % 30) * TILE_SIZE - TILE_SIZE
    return x_coordinate
def y_position(pos_number):
    if (pos_number % 30) == 0:
        y_coordinate = (int(pos_number / 30)) * TILE_SIZE - TILE_SIZE
    else:
        y_coordinate = (int(pos_number / 30)) * TILE_SIZE
    return y_coordinate

# Bilder laden
player_image = pygame.image.load('astronaut.png').convert_alpha()  # Pfad zum Astronautenbild
granit_image = pygame.image.load('granit.png').convert_alpha()  # Pfad zum Granitbild
stone_image = pygame.image.load('stone.png').convert_alpha()  # Pfad zum Stonebild
bomb_image = pygame.image.load('bomb.png').convert_alpha()  # Pfad zum Bombbild
enemy_image = pygame.image.load('enemy.png').convert_alpha()  # Pfad zum Gegnerbild
rocket_image = pygame.image.load('rocket.png').convert_alpha()  # Pfad zum Raketenbild
background_image = pygame.image.load('background.png').convert_alpha()  # Pfad zum Hintergrund

# Musik laden
pygame.mixer.music.load("stoneworld_battle.mp3")
bombsound = pygame.mixer.Sound('bomb.wav')

# Musik initialisieren
pygame.mixer.music.play(-1)  # -1 bedeutet, in Endlosschleife
pygame.mixer.music.set_volume(0.1)  # Lautstärke Hintergrundmusik von 0.0 bis 1.0
bombsound.set_volume(0.2)  # Lautstärke Bombe

# Spielerklasse definieren
class Player:
    def __init__(self, x, y):
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def update_movement(self, keys):
        self.move_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.move_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        self.move_up = keys[pygame.K_UP] or keys[pygame.K_w]
        self.move_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

    def move(self, keys, hindernisse):
        #original_rect = self.rect.copy()

        # Bewegung in jede Richtung separat überprüfen
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            new_rect = self.rect.copy()
            new_rect.x -= self.speed
            if not self.check_collision(new_rect, hindernisse):
                self.rect = new_rect

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            new_rect = self.rect.copy()
            new_rect.x += self.speed
            if not self.check_collision(new_rect, hindernisse):
                self.rect = new_rect

        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            new_rect = self.rect.copy()
            new_rect.y -= self.speed
            if not self.check_collision(new_rect, hindernisse):
                self.rect = new_rect

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            new_rect = self.rect.copy()
            new_rect.y += self.speed
            if not self.check_collision(new_rect, hindernisse):
                self.rect = new_rect

    def check_collision(self, rect, hindernisse):
        for hindernis in hindernisse:
            if rect.colliderect(hindernis.rect) or rect.x < 0 or rect.x > GAME_SCREEN_WIDTH - PLAYER_SIZE or rect.y < 0 or rect.y > GAME_SCREEN_HEIGHT - PLAYER_SIZE :
                return True
        return False

# Spielerinstanz erstellen und auf Spielfeld positionieren
player = Player(player_x_position(PLAYER_START_POSITION), player_y_position(PLAYER_START_POSITION))

# Gegnerklasse definieren
class Enemy:
    def __init__(self, x, y):
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = ENEMY_SPEED
        self.direction = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        self.last_direction_change_time = pygame.time.get_ticks()  # Zeitpunkt des letzten Richtungswechsels

    def move(self, hindernisse):
        current_time = pygame.time.get_ticks()
        new_rect = self.rect.copy()

        # Richtung regelmäßig ändern, wenn die Zeit abgelaufen ist
        if current_time - self.last_direction_change_time >= ENEMY_DIRECTION_CHANGE_INTERVAL:
            self.change_direction()
            self.last_direction_change_time = current_time

        # Bewegung basierend auf der Richtung
        if self.direction == 'LEFT':
            new_rect.x -= self.speed
            # Kollision mit dem linken Rand
            if new_rect.x < 0:
                new_rect.x = 0
                self.change_direction()

        if self.direction == 'RIGHT':
            new_rect.x += self.speed
            # Kollision mit dem rechten Rand
            if new_rect.x > GAME_SCREEN_WIDTH - TILE_SIZE:
                new_rect.x = GAME_SCREEN_WIDTH - TILE_SIZE
                self.change_direction()

        if self.direction == 'UP':
            new_rect.y -= self.speed
            # Kollision mit dem oberen Rand
            if new_rect.y < 0:
                new_rect.y = 0
                self.change_direction()

        if self.direction == 'DOWN':
            new_rect.y += self.speed
            # Kollision mit dem unteren Rand
            if new_rect.y > GAME_SCREEN_HEIGHT - TILE_SIZE:
                new_rect.y = GAME_SCREEN_HEIGHT - TILE_SIZE
                self.change_direction()

        # Kollision prüfen und Richtung ändern, wenn eine Kollision vorliegt
        if self.check_collision(new_rect, hindernisse):
            self.change_direction()
        else:
            self.rect = new_rect

    def check_collision(self, rect, hindernisse):
        for hindernis in hindernisse:
            if rect.colliderect(hindernis.rect):
                return True
        return False

    def change_direction(self):
        self.direction = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Klasse Granit
class Granit:
    def __init__(self, x, y):
        self.image = granit_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(granit.image, granit.rect.topleft)

class Stone:
    def __init__(self, x, y):
        self.image = stone_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(stone.image, stone.rect.topleft)

# Klasse Bombe
class Bomb:
    def __init__(self, x, y):
        self.image = bomb_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x + 5, y + 5)
        self.time_placed = pygame.time.get_ticks()
        self.exploded = False

    def draw(self, screen):
        screen.blit(bomb.image, bomb.rect.topleft)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.time_placed >= BOMB_TIME:
            self.exploded = True

# Liste von Hindernissen erstellen aus Liste GRANIT_POSITIONS
granits = []
for i in range(len(GRANIT_POSITIONS)):
    granits.append(Granit(x_position(GRANIT_POSITIONS[i]), y_position(GRANIT_POSITIONS[i])))

# Liste von Hindernissen erstellen aus Liste STONE_POSITIONS
stones = []
for i in range(len(STONE_POSITIONS)):
    stones.append(Stone(x_position(STONE_POSITIONS[i]), y_position(STONE_POSITIONS[i])))

# Liste von Bomben
bombs = []

# Liste von Gegnern
enemies = []
for i in range(len(ENEMY_POSITIONS)):
    enemies.append(Enemy(x_position(ENEMY_POSITIONS[i]), y_position(ENEMY_POSITIONS[i])))

# Funktion zur Überprüfung der Kollision mit bestehenden Bomben und Hindernissen
def can_place_bomb(x, y, bombs, hindernisse):
    test_rect = pygame.Rect(x + 5, y + 5, PLAYER_SIZE, PLAYER_SIZE)
    for bomb in bombs:
        if test_rect.colliderect(bomb.rect):
            return False
    for hindernis in hindernisse:
        if test_rect.colliderect(hindernis.rect):
            return False
    return True

# Funktion, um Steine zu zerstören, wenn sie in der Nähe einer explodierten Bombe sind
def check_bomb_explosion_effect(bombs, stones):
    global PLAYER_SCORE
    for bomb in bombs:
        if bomb.exploded:
            # Erzeuge eine Liste von Rects, die den Explosionseffekt darstellen (rechts, links, oben, unten der Bombe)
            explosion_rects = [
                pygame.Rect(bomb.rect.x + PLAYER_SIZE, bomb.rect.y, PLAYER_SIZE, PLAYER_SIZE),  # Rechts
                pygame.Rect(bomb.rect.x - PLAYER_SIZE, bomb.rect.y, PLAYER_SIZE, PLAYER_SIZE),  # Links
                pygame.Rect(bomb.rect.x, bomb.rect.y + PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE),  # Unten
                pygame.Rect(bomb.rect.x, bomb.rect.y - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)   # Oben
            ]

            # Explosion abspielen
            bombsound.play()

            # Überprüfe auf Kollision mit Steinen und entferne die Steine
            destroyed_stones = [stone for stone in stones if any(explosion_rect.colliderect(stone.rect) for explosion_rect in explosion_rects)]
            PLAYER_SCORE += len(destroyed_stones) * SCORE_VALUE_STONE  # Punkte basierend auf der Anzahl zerstörter Steine vergeben
            stones[:] = [stone for stone in stones if stone not in destroyed_stones]

            ############################################
            # Zeichne die Explosionen visuell auf dem Bildschirm
            for explosion_rect in explosion_rects:
                pygame.draw.rect(screen, RED, explosion_rect)  # Explosion visuell darstellen
            ###########################################

# Startbildschirm-Funktion
def show_start_screen():
    screen.fill(BACKGROUND)

    # Titeltext rendern
    title_text = title_font.render("Cometbomber", True, BLACK)
    title_rect = title_text.get_rect(center=(GAME_SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

    # Anweisungstext rendern
    instruction_text = instruction_font.render("Drücke LEERTASTE, um zu starten", True, BLACK)
    instruction_rect = instruction_text.get_rect(center=(GAME_SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    # Text auf dem Bildschirm zeichnen
    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)

    pygame.display.flip()

    # Warten auf die Eingabe des Spielers
    waiting = True
    while waiting:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Escape-Taste gedrückt
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Start des Spiels bei Drücken der Leertaste
                    waiting = False
        # Tasteneingaben abfragen
        keys = pygame.key.get_pressed()

        # Spiel beenden
        if keys[pygame.K_ESCAPE]:  # Escape-Taste gedrückt
            running = False  # Spiel beenden

def show_game_over_screen():
    screen.fill(BLACK)

    # Game-Over-Text rendern
    game_over_text = title_font.render("Game Over", True, RED)
    game_over_rect = game_over_text.get_rect(center=(GAME_SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))

    # Anweisungstext rendern
    instruction_text = instruction_font.render("Drücke R, um das Spiel neu zu starten", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(GAME_SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    # Score rendern
    score_text = title_font.render(f'Score: {PLAYER_SCORE}', True, RED)
    score_rect = score_text.get_rect(center=(GAME_SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    # Text auf dem Bildschirm zeichnen
    screen.blit(game_over_text, game_over_rect)
    screen.blit(instruction_text, instruction_rect)
    screen.blit(score_text, score_rect)

    pygame.display.flip()

    # Warten auf die Eingabe des Spielers (R für Neustart)
    waiting = True
    while waiting:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Escape-Taste gedrückt
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Spiel neustarten bei Drücken von 'R'
                    waiting = False

def show_winner_screen():
    # Bildschirm schwarz füllen
    screen.fill(BLACK)

    # Winner Text rendern
    winner_text = title_font.render("Winner", True, RED)
    winner_rect = winner_text.get_rect(center=(GAME_SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))

    # Anweisungstext rendern
    instruction_text = instruction_font.render("Drücke R, um das Spiel neu zu starten", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(GAME_SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    # Score rendern
    score_text = title_font.render(f'Score: {PLAYER_SCORE}', True, RED)
    score_rect = score_text.get_rect(center=(GAME_SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    # Text auf dem Bildschirm zeichnen
    screen.blit(winner_text, winner_rect)
    screen.blit(instruction_text, instruction_rect)
    screen.blit(score_text, score_rect)

    pygame.display.flip()

    # Warten auf die Eingabe des Spielers (R für Neustart)
    waiting = True
    while waiting:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Escape-Taste gedrückt
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Spiel neustarten bei Drücken von 'R'
                    waiting = False

# Startbildschirm anzeigen
show_start_screen()

# Ziel erstellen
goal_rect = pygame.Rect(GAME_SCREEN_WIDTH - 15, GAME_SCREEN_HEIGHT - 15, 15, 15)

# Hauptspiel-Schleife
operational = True
running = True
gameover = False
winner = False
while operational:
    while running:
        # Ereignisse abfragen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                operational = False

            # Bombe platzieren bei Tastendruck SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and len(bombs) <= PLAYER_BOMB_MAXIMUM - 1 :
                bomb_x = (player.rect.x // TILE_SIZE) * TILE_SIZE
                bomb_y = (player.rect.y // TILE_SIZE) * TILE_SIZE
                if can_place_bomb(bomb_x, bomb_y, bombs, granits + stones):
                    bombs.append(Bomb(bomb_x, bomb_y))

        # Tasteneingaben abfragen
        keys = pygame.key.get_pressed()

        # Spiel beenden
        if keys[pygame.K_ESCAPE]:  # Escape-Taste gedrückt
            sys.exit()

        # Spielerbewegung abfragen
        player.move(keys, granits + stones)

        # Gegnerbewegung abfragen
        for enemy in enemies:
            enemy.move(granits + stones)

        # Ziel zeichnen
        pygame.draw.rect(screen, BACKGROUND, goal_rect)

        # Hintergrund zeichnen
        for i in range( ( ( int( GAME_SCREEN_WIDTH / TILE_SIZE) + 1 ) * int( GAME_SCREEN_HEIGHT / TILE_SIZE) ) ):
            screen.blit(background_image, ( x_position(i), y_position(i) ) )

        # Rakete zeichnen
        screen.blit(rocket_image, (GAME_SCREEN_WIDTH - TILE_SIZE, GAME_SCREEN_HEIGHT - TILE_SIZE))

        # Bomben aktualisieren und zeichnen
        for bomb in bombs:
            bomb.update()
            if bomb.exploded:
                # Explosion visuell darstellen
                for explosion_rect in [
                    pygame.Rect(bomb.rect.x, bomb.rect.y, PLAYER_SIZE, PLAYER_SIZE),  # Bombe selbst
                    pygame.Rect(bomb.rect.x + PLAYER_SIZE, bomb.rect.y, PLAYER_SIZE, PLAYER_SIZE),  # Rechts
                    pygame.Rect(bomb.rect.x - PLAYER_SIZE, bomb.rect.y, PLAYER_SIZE, PLAYER_SIZE),  # Links
                    pygame.Rect(bomb.rect.x, bomb.rect.y + PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE),  # Unten
                    pygame.Rect(bomb.rect.x, bomb.rect.y - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)  # Oben
                ]:
                    pygame.draw.rect(screen, RED, explosion_rect)  # Explosion visuell darstellen
            else:
                bomb.draw(screen)

        # Überprüfe die Explosionseffekte der Bomben auf Steine
        check_bomb_explosion_effect(bombs, stones)


        # Überprüfen, ob der Spieler mit einem Gegner kollidiert
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                running = False  # Spiel beenden
                gameover = True

        # Überprüfen, ob der Spieler von einer Bombenexplosion getroffen wird
        for bomb in bombs:
            if bomb.exploded:
                explosion_rects = [
                    bomb.rect,
                    pygame.Rect(bomb.rect.x + PLAYER_SIZE, bomb.rect.y, PLAYER_SIZE, PLAYER_SIZE),  # Rechts
                    pygame.Rect(bomb.rect.x - PLAYER_SIZE, bomb.rect.y, PLAYER_SIZE, PLAYER_SIZE),  # Links
                    pygame.Rect(bomb.rect.x, bomb.rect.y + PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE),  # Unten
                    pygame.Rect(bomb.rect.x, bomb.rect.y - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)  # Oben
                ]
                for explosion_rect in explosion_rects:
                    if player.rect.colliderect(explosion_rect):
                        gameover = True
                        running = False  # Spiel beenden

        # Alle explodierten Bomben aus der Liste entfernen
        bombs = [bomb for bomb in bombs if not bomb.exploded]

        # Spieler zeichnen
        screen.blit(player.image, player.rect.topleft)

        # Granits zeichnen
        for granit in granits:
            granit.draw(screen)

        #Stones zeichnen
        for stone in stones:
            stone.draw(screen)

        # Gegner zeichnen
        for enemy in enemies:
            enemy.draw(screen)

        # Infobar zeichnen
        pygame.draw.rect(screen, GRAY, (0, 680, 1160, 40))

        # Punkte anzeigen
        score_text = infobar_font.render(f"Score: {PLAYER_SCORE}", True, WHITE)
        screen.blit(score_text, (1050, 688))  # Punkte oben links anzeigen

        # Überprüfen, ob der Spieler das Ziel erreicht hat
        if player.rect.colliderect(goal_rect):
            running = False
            winner = True


        # Aktuelle Zeit berechnen
        current_time = pygame.time.get_ticks()

        # Restzeit berechnen
        time_left = (GAME_DURATION - (current_time - start_time)) // 1000  # In Sekunden umrechnen

        # Timer auf dem Bildschirm anzeigen
        timer_text = infobar_font.render(f"Time: {time_left}", True, WHITE)
        screen.blit(timer_text, (900, 688))  # Timer auf dem Bildschirm anzeigen

        # Spiel beenden, wenn die Zeit abgelaufen ist
        if current_time - start_time >= GAME_DURATION:
            running = False
            gameover = True

        # Bildschirm aktualisieren
        pygame.display.flip()

        # Frame-Rate begrenzen (60 FPS)
        clock.tick(60)

    #GameOver Screen anzeigen und Variablen zurücksetzen
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                operational = False

        #Zeige Game Over Screen
        show_game_over_screen()

        # Variablen zurücksetzen, um das Spiel neu zu starten
        player = Player(player_x_position(PLAYER_START_POSITION), player_y_position(PLAYER_START_POSITION))
        bombs = []

        PLAYER_SCORE = 0
        start_time = pygame.time.get_ticks()

        for i in range(len(STONE_POSITIONS)):
            stones.append(Stone(x_position(STONE_POSITIONS[i]), y_position(STONE_POSITIONS[i])))

        # Spiel wieder starten
        running = True
        gameover = False

    while winner:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                operational = False

        # Winner Screen anzeigen
        show_winner_screen()

        # Variablen zurücksetzen, um das Spiel neu zu starten
        player = Player(player_x_position(PLAYER_START_POSITION), player_y_position(PLAYER_START_POSITION))
        bombs = []
        PLAYER_SCORE = 0
        start_time = pygame.time.get_ticks()

        for i in range(len(STONE_POSITIONS)):
            stones.append(Stone(x_position(STONE_POSITIONS[i]), y_position(STONE_POSITIONS[i])))

        # Spiel wieder starten
        running = True
        winner = False


pygame.quit()