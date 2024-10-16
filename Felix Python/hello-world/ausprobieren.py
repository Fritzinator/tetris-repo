import pygame
import sys

# Initialisieren von Pygame
pygame.init()

# Fenstergröße
WIDTH, HEIGHT = 500, 500

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)
Clock = pygame.time.Clock()

# Erstellen eines Fensters
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Fenster")

# Quadratposition und Größe
square1_x = 200
square1_y = 200
square_size = 50

# Zweites Quadratposition und Größe
square2_x = 300
square2_y = 300
square2_visible = True

# Haupt-Loop
run = True
while run:
    delta_time = Clock.tick(250) / 1000
    # Ereignisse verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Quadrat 1 bewegen (mit den Pfeiltasten)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        square1_x -= 1
    if keys[pygame.K_RIGHT]:
        square1_x += 1
    if keys[pygame.K_UP]:
        square1_y -= 1
    if keys[pygame.K_DOWN]:
        square1_y += 1

    # Kollisionserkennung
    if (square1_x < square2_x + square_size and
            square1_x + square_size > square2_x and
            square1_y < square2_y + square_size and
            square1_y + square_size > square2_y):
        # Quadrat 2 verschwinden lassen
        square2_visible = False
    else:
        # Quadrat 2 sichtbar machen
        square2_visible = True

    # Hintergrund zeichnen
    win.fill(WHITE)

    # Quadrat 1 zeichnen
    pygame.draw.rect(win, RED, (square1_x, square1_y, square_size, square_size))

    # Quadrat 2 zeichnen, wenn sichtbar
    if square2_visible:
        pygame.draw.rect(win, RED, (square2_x, square2_y, square_size, square_size))

    # Update anzeigen
    pygame.display.update()

# Pygame beenden
pygame.quit()
sys.exit()
