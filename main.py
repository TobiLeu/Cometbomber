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
PLAYER_START_POSITION = 70  # Startposition des Spielers
GRANIT_POSITIONS = [75, 95, 105, 150, 200, 221, 256, 287]  # Granit = nicht zerstörbares Hindernis
STONE_POSITIONS = [76,96,106] # Stone = zerstörbares Hindernis

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Bildschirm einrichten
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cometbomber")

# Spieluhr
clock = pygame.time.Clock()

# Funktionen Spielfeld in Rastereinteilung: x-Koordinate, y-Koordinate
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

# Spielerklasse definieren
class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE)
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
player = Player(x_position(PLAYER_START_POSITION), y_position(PLAYER_START_POSITION))

# Klasse Granit
class Granit:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

class Stone:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

# Liste von Hindernissen erstellen aus Liste GRANIT_POSITIONS
granits = []
for i in range(len(GRANIT_POSITIONS)):
    granits.append(Granit(x_position(GRANIT_POSITIONS[i]), y_position(GRANIT_POSITIONS[i])))

# Liste von Hindernissen erstellen aus Liste STONE_POSITIONS
stones = []
for i in range(len(STONE_POSITIONS)):
    stones.append(Stone(x_position(STONE_POSITIONS[i]), y_position(STONE_POSITIONS[i])))


# Hauptspiel-Schleife
running = True
while running:
    # Ereignisse abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tasteneingaben abfragen
    keys = pygame.key.get_pressed()

    # Spiel beenden
    if keys[pygame.K_ESCAPE]:  # Escape-Taste gedrückt
        running = False  # Spiel beenden

    # Spielerbewegung abfragen
    player.move(keys, granits + stones)

    # Bildschirm mit schwarzer Farbe füllen
    screen.fill(BLACK)

    # Spieler zeichnen
    screen.blit(player.image, player.rect.topleft)

    # Granits zeichnen
    for granit in granits:
        granit.draw(screen)

    #Stones zeichnen
    for stone in stones:
        stone.draw(screen)

    # Bildschirm aktualisieren
    pygame.display.flip()

    # Frame-Rate begrenzen (60 FPS)
    clock.tick(60)

pygame.quit()
'''
import pygame

# Initialisiere Pygame
pygame.init()

# Spielkonstanten
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
TILE_SIZE = 40
PLAYER_SPEED = 5
BOMB_TIME = 3000  # Zeit bis zur Explosion in Millisekunden
EXPLOSION_DURATION = 500  # Dauer der Explosion in Millisekunden
PLAYER_START_POSITION = 70  # Startposition des Spielers
GRANIT_POSITIONS = [75, 95, 105, 150, 200, 221, 256, 287]  # Granit = nicht zerstörbares Hindernis
STONE_POSITIONS = [100, 120, 140, 160, 180]  # Stone = weiteres Hindernis

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Bildschirm einrichten
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cometbomber")

# Spieluhr
clock = pygame.time.Clock()

# Funktionen Spielfeld in Rastereinteilung: x-Koordinate, y-Koordinate
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

# Spielerklasse definieren
class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    # Spielerbewegung innerhalb des Spielfeldes
    def move(self, keys, hindernisse):
        # Erstelle eine Kopie des aktuellen Rects
        new_rect = self.rect.copy()

        # Bewegung vorbereiten
        if keys[pygame.K_LEFT] and new_rect.x > 0:
            new_rect.x -= self.speed
        if keys[pygame.K_RIGHT] and new_rect.x < (SCREEN_WIDTH - TILE_SIZE):
            new_rect.x += self.speed
        if keys[pygame.K_UP] and new_rect.y > 0:
            new_rect.y -= self.speed
        if keys[pygame.K_DOWN] and new_rect.y < (SCREEN_HEIGHT - TILE_SIZE):
            new_rect.y += self.speed

        # Kollision überprüfen
        if not self.check_collision(new_rect, hindernisse):
            self.rect = new_rect  # Bewegung ausführen, wenn keine Kollision vorliegt

    # Methode zur Kollisionserkennung
    def check_collision(self, rect, hindernisse):
        for hindernis in hindernisse:
            if rect.colliderect(hindernis.rect):
                return True
        return False

# Spielerinstanz erstellen und auf Spielfeld positionieren
player = Player(x_position(PLAYER_START_POSITION), y_position(PLAYER_START_POSITION))

# Klasse Hindernis Granit
class Granit:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

# Klasse Hindernis Stone
class Stone:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)

# Liste von Hindernissen erstellen aus Liste GRANIT_POSITIONS
granits = []
for i in range(len(GRANIT_POSITIONS)):
    granits.append(Granit(x_position(GRANIT_POSITIONS[i]), y_position(GRANIT_POSITIONS[i])))

# Liste von Steinen erstellen aus Liste STONE_POSITIONS
stones = []
for i in range(len(STONE_POSITIONS)):
    stones.append(Stone(x_position(STONE_POSITIONS[i]), y_position(STONE_POSITIONS[i])))

# Hauptspiel-Schleife
running = True
while running:
    # Ereignisse abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tasteneingaben abfragen
    keys = pygame.key.get_pressed()

    # Spiel beenden
    if keys[pygame.K_ESCAPE]:  # Escape-Taste gedrückt
        running = False  # Spiel beenden

    # Spielerbewegung abfragen
    player.move(keys, granits + stones)  # Überprüfe Kollision mit Granit und Stein

    # Bildschirm mit schwarzer Farbe füllen
    screen.fill(BLACK)

    # Spieler zeichnen
    screen.blit(player.image, player.rect.topleft)

    # Alle Hindernisse zeichnen
    for granit in granits:
        granit.draw(screen)

    # Alle Steine zeichnen
    for stone in stones:
        stone.draw(screen)

    # Bildschirm aktualisieren
    pygame.display.flip()

    # Frame-Rate begrenzen (60 FPS)
    clock.tick(60)

pygame.quit()'''