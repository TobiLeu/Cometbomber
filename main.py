import pygame

# Initialisiere Pygame
pygame.init()

# Spielkonstanten
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
TILE_SIZE = 40
PLAYER_SPEED = 5
PLAYER_SIZE = 30
BOMB_TIME = 3000  # Zeit bis zur Explosion in Millisekunden
EXPLOSION_DURATION = 500  # Dauer der Explosion in Millisekunden
PLAYER_START_POSITION = 1  # Startposition des Spielers
GRANIT_POSITIONS = [75, 95, 105, 150, 200, 221, 256, 287]  # Granit = nicht zerstörbares Hindernis
STONE_POSITIONS = [76,96,106] # Stone = zerstörbares Hindernis

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

# Spielerklasse definieren
class Player:
    def __init__(self, x, y):
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

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

    # Bildschirm aktualisieren
    pygame.display.flip()

    # Frame-Rate begrenzen (60 FPS)
    clock.tick(60)

pygame.quit()
