import pygame
import random

# Initialisiere Pygame
pygame.init()

# Spielkonstanten
SCREEN_WIDTH = 1160
SCREEN_HEIGHT = 680
TILE_SIZE = 40
PLAYER_SPEED = 5
ENEMY_SPEED = 1
PLAYER_SIZE = 30
BOMB_TIME = 3000  # Zeit bis zur Explosion in Millisekunden
EXPLOSION_DURATION = 500  # Dauer der Explosion in Millisekunden
PLAYER_START_POSITION = 1  # Startposition des Spielers
GRANIT_POSITIONS = [32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58,
                    92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118,
                    152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178,
                    212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238,
                    272, 274, 276, 278, 280, 282, 284, 286, 288, 290, 292, 294, 296, 298,
                    332, 334, 336, 338, 340, 342, 344, 346, 348, 350, 352, 354, 356, 358,
                    392, 394, 396, 398, 400, 402, 404, 406, 408, 410, 412, 414, 416, 418,
                    452, 454, 456, 458, 460, 462, 464, 466, 468, 470, 472, 474, 476, 478]  # Granit = nicht zerstörbares Hindernis
STONE_POSITIONS = [33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 62, 64, 66, 68, 70,
                   #72, 74, 76, 78, 80, 82, 84, 86, 88, 93, 95, 97, 99, 101, 103, 105, 107,
                   109, 111, 113, 115, 117, 122, 124, 126, 128, 130, 132, 134, 136, 138,
                   #140, 142, 144, 146, 148, 153, 155, 157, 159, 161, 163, 165, 167, 169,
                   171, 173, 175, 177, 182, 184, 186, 188, 190, 192, 194, 196, 198, 200,
                   #202, 204, 206, 208, 213, 215, 217, 219, 221, 223, 225, 227, 229, 231,
                   233, 235, 237, 242, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262,
                  #264, 266, 268, 273, 275, 277, 279, 281, 283, 285, 287, 289, 291, 293,
                   #295, 297, 302, 304, 306, 308, 310, 312, 314, 316, 318, 320, 322, 324,
                   326, 328, 333, 335, 337, 339, 341, 343, 345, 347, 349, 351, 353, 355,
                   357, 362, 364, 366, 368, 370, 372, 374, 376, 378, 380, 382, 384, 386,
                  # 388, 393, 395, 397, 399, 401, 403, 405, 407, 409, 411, 413, 415, 417,
                  # 422, 424, 426, 428, 430, 432, 434, 436, 438, 440, 442, 444, 446, 448,
                   453, 455, 457, 459, 461, 463, 465, 467, 469, 471, 473, 475, 477] # Stone = zerstörbares Hindernis
ENEMY_POSITIONS = [80,205]
ENEMY_DIRECTION_CHANGE_INTERVAL = 2000  # Zeit in Millisekunden

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND = (244, 164, 96)

# Bildschirm einrichten
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cometbomber")

# Spieluhr
clock = pygame.time.Clock()

# Funktionen Spielfeld in Rastereinteilung: x-Koordinate, y-Koordinate
def player_x_position(pos_number):
    if (pos_number % 30) == 0:
        x_coordinate = (pos_number % 30) * TILE_SIZE + SCREEN_WIDTH - TILE_SIZE
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
        x_coordinate = (pos_number % 30) * TILE_SIZE + SCREEN_WIDTH - TILE_SIZE
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

    # Spielerbewegung innerhalb des Spielfeldes
    def move(self, keys, hindernisse):
        new_rect = self.rect.copy()  # Erstelle eine Kopie des aktuellen Rects

        # Bewegung vorbereiten
        if (keys[pygame.K_LEFT] and new_rect.x > 0) or (keys[pygame.K_a] and new_rect.x > 0):
            new_rect.x -= self.speed
        if (keys[pygame.K_RIGHT] and new_rect.x < (SCREEN_WIDTH - TILE_SIZE)) or (keys[pygame.K_d] and new_rect.x < (SCREEN_WIDTH - TILE_SIZE)):
            new_rect.x += self.speed
        if (keys[pygame.K_UP] and new_rect.y > 0) or (keys[pygame.K_w] and new_rect.y > 0):
            new_rect.y -= self.speed
        if (keys[pygame.K_DOWN] and new_rect.y < (SCREEN_HEIGHT - TILE_SIZE)) or (keys[pygame.K_s] and new_rect.y < (SCREEN_HEIGHT - TILE_SIZE)):
            new_rect.y += self.speed

        # Kollision überprüfen
        if not self.check_collision(new_rect, hindernisse):
            self.rect = new_rect  # Bewegung ausführen, wenn keine Kollision vorliegt


    def check_collision(self, rect, hindernisse):
        for hindernis in hindernisse:
            if rect.colliderect(hindernis.rect):
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
            if new_rect.x > SCREEN_WIDTH - TILE_SIZE:
                new_rect.x = SCREEN_WIDTH - TILE_SIZE
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
            if new_rect.y > SCREEN_HEIGHT - TILE_SIZE:
                new_rect.y = SCREEN_HEIGHT - TILE_SIZE
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
#enemies = [Enemy(x_position(random.randint(1, 29)), y_position(random.randint(1, 17))) for _ in range(5)]
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


# Hauptspiel-Schleife
running = True
while running:
    # Ereignisse abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Bombe platzieren bei Tastendruck SPACE
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bomb_x = (player.rect.x // TILE_SIZE) * TILE_SIZE
            bomb_y = (player.rect.y // TILE_SIZE) * TILE_SIZE
            if can_place_bomb(bomb_x, bomb_y, bombs, granits + stones):
                bombs.append(Bomb(bomb_x, bomb_y))



    # Tasteneingaben abfragen
    keys = pygame.key.get_pressed()

    # Spiel beenden
    if keys[pygame.K_ESCAPE]:  # Escape-Taste gedrückt
        running = False  # Spiel beenden

    # Spielerbewegung abfragen
    player.move(keys, granits + stones)

    # Gegnerbewegung abfragen
    for enemy in enemies:
        enemy.move(granits + stones)

    # Bildschirm mit Hintergrundfarbe füllen
    screen.fill(BACKGROUND)

    # Spieler zeichnen
    screen.blit(player.image, player.rect.topleft)

    # Granits zeichnen
    for granit in granits:
        granit.draw(screen)

    #Stones zeichnen
    for stone in stones:
        stone.draw(screen)

    # Bomben aktualisieren und zeichnen
    for bomb in bombs:
        bomb.update()
        if bomb.exploded:
            pygame.draw.rect(screen, RED, bomb.rect)  # Explosion visuell darstellen
        else:
            bomb.draw(screen)

    # Alle explodierten Bomben aus der Liste entfernen
    bombs = [bomb for bomb in bombs if not bomb.exploded]

    # Gegner zeichnen
    for enemy in enemies:
        enemy.draw(screen)

    # Überprüfen, ob der Spieler mit einem Gegner kollidiert
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            running = False  # Spiel beenden, wenn eine Kollision erkannt wird

    # Bildschirm aktualisieren
    pygame.display.flip()

    # Frame-Rate begrenzen (60 FPS)
    clock.tick(60)

pygame.quit()
