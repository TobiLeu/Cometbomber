#Dies ist ein Test, ob das Arbeiten über Github funktioniert.
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
PLAYER_START_POSITION = 70 # Startposition des Spielers
GRANIT_POSITIONS = [75,95,105,150,200,221,256,287] # Granit = nichtzerstörbares Hindernis

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

#Funktionen Spielfeld in Rastereinteilung: x-Koordinate, y-Koordinate
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
        y_coordinate =  (int(pos_number / 30)) * TILE_SIZE
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
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < (SCREEN_WIDTH - TILE_SIZE):
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < (SCREEN_HEIGHT - TILE_SIZE) :
            self.rect.y += self.speed

# Spielerinstanz erstellen und auf Spielfeld positionieren
player = Player(x_position(PLAYER_START_POSITION), y_position(PLAYER_START_POSITION))

# Klasse Hindernis
class Granit:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

# Liste von Hindernissen erstellen aus Liste GRANIT_POSITIONS
granits = []
for i in range(len(GRANIT_POSITIONS)):
    granits.append(Granit(x_position(GRANIT_POSITIONS[i]),y_position(GRANIT_POSITIONS[i])))



# Hauptspiel-Schleife
running = True
while running:
    # Ereignisse abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tasteneingaben abfragen
    keys = pygame.key.get_pressed()

    #Spiel beenden
    if keys[pygame.K_ESCAPE]:  # Escape-Taste gedrückt
        running = False  # Spiel beenden

    #Spielerbewegung abfragen
    player.move(keys)

    # Bildschirm mit schwarzer Farbe füllen
    screen.fill(BLACK)
    
    # Spieler zeichnen
    screen.blit(player.image, player.rect.topleft)

    # Alle Hindernisse zeichnen
    for granit in granits:
        granit.draw(screen)

    # Bildschirm aktualisieren
    pygame.display.flip()

    # Frame-Rate begrenzen (60 FPS)
    clock.tick(60)

pygame.quit()

