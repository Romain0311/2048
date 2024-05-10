import pygame
import random

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 128, 0)
BLUE = (0, 0, 128)
CELL_COLORS = {
    0: GRAY,
    2: (255, 255, 128),
    4: (255, 255, 0),
    8: (255, 128, 0),
    16: (255, 128, 128),
    32: (255, 0, 0),
    64: (255, 0, 255),
    128: (128, 255, 128),
    256: (128, 255, 255),
    512: (128, 128, 255),
    1024: (128, 0, 255),
    2048: (128, 0, 128)
}

# Définition des constantes pour la taille de la fenêtre et de la grille
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 4
CELL_SIZE = 100
MARGIN = 10
GRID_WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * MARGIN

# Définition des constantes pour les polices
FONT_SIZE = 40
FONT = pygame.font.SysFont(None, FONT_SIZE)

# Définition des constantes pour les directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Fonction pour dessiner la grille
def draw_grid(screen, grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_rect = pygame.Rect((MARGIN + CELL_SIZE) * j + MARGIN, (MARGIN + CELL_SIZE) * i + MARGIN, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, CELL_COLORS[grid[i][j]], cell_rect)
            if grid[i][j] != 0:
                cell_text = FONT.render(str(grid[i][j]), True, BLACK)
                text_rect = cell_text.get_rect(center=cell_rect.center)
                screen.blit(cell_text, text_rect)

# Fonction pour générer un nouveau nombre aléatoire dans la grille
def generate_random_number(grid):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])

# Fonction pour déplacer les nombres dans la grille
def move_numbers(grid, direction):
    moved = False
    if direction == UP:
        for j in range(GRID_SIZE):
            for i in range(1, GRID_SIZE):
                for k in range(i, 0, -1):
                    if grid[k][j] != 0 and grid[k - 1][j] == 0:
                        grid[k - 1][j], grid[k][j] = grid[k][j], grid[k - 1][j]
                        moved = True
                    elif grid[k][j] != 0 and grid[k - 1][j] == grid[k][j]:
                        grid[k - 1][j] *= 2
                        grid[k][j] = 0
                        moved = True
    elif direction == DOWN:
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE - 2, -1, -1):
                for k in range(i, GRID_SIZE - 1):
                    if grid[k][j] != 0 and grid[k + 1][j] == 0:
                        grid[k + 1][j], grid[k][j] = grid[k][j], grid[k + 1][j]
                        moved = True
                    elif grid[k][j] != 0 and grid[k + 1][j] == grid[k][j]:
                        grid[k + 1][j] *= 2
                        grid[k][j] = 0
                        moved = True
    elif direction == LEFT:
        for i in range(GRID_SIZE):
            for j in range(1, GRID_SIZE):
                for k in range(j, 0, -1):
                    if grid[i][k] != 0 and grid[i][k - 1] == 0:
                        grid[i][k - 1], grid[i][k] = grid[i][k], grid[i][k - 1]
                        moved = True
                    elif grid[i][k] != 0 and grid[i][k - 1] == grid[i][k]:
                        grid[i][k - 1] *= 2
                        grid[i][k] = 0
                        moved = True
    elif direction == RIGHT:
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 2, -1, -1):
                for k in range(j, GRID_SIZE - 1):
                    if grid[i][k] != 0 and grid[i][k + 1] == 0:
                        grid[i][k + 1], grid[i][k] = grid[i][k], grid[i][k + 1]
                        moved = True
                    elif grid[i][k] != 0 and grid[i][k + 1] == grid[i][k]:
                        grid[i][k + 1] *= 2
                        grid[i][k] = 0
                        moved = True
    return moved

# Fonction pour vérifier si le joueur a perdu
def check_loss(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return False
            if i < GRID_SIZE - 1 and grid[i][j] == grid[i + 1][j]:
                return False
            if j < GRID_SIZE - 1 and grid[i][j] == grid[i][j + 1]:
                return False
    return True

# Création de la grille de jeu
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Génération de deux nombres aléatoires pour commencer
generate_random_number(grid)
generate_random_number(grid)

# Création de la fenêtre de jeu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Game")

# Boucle principale du jeu
running = True
while running:
    screen.fill(WHITE)

    # Dessiner la grille
    draw_grid(screen, grid)

    # Vérifier si le joueur a perdu
    if check_loss(grid):
        loss_text = FONT.render("You Lost!", True, BLUE)
        screen.blit(loss_text, ((WIDTH - loss_text.get_width()) / 2, HEIGHT - 50))

    # Actualiser l'écran
    pygame.display.flip()

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                moved = move_numbers(grid, UP)
            elif event.key == pygame.K_DOWN:
                moved = move_numbers(grid, DOWN)
            elif event.key == pygame.K_LEFT:
                moved = move_numbers(grid, LEFT)
            elif event.key == pygame.K_RIGHT:
                moved = move_numbers(grid, RIGHT)

            # Générer un nouveau nombre aléatoire si le mouvement a été effectué
            if moved:
                generate_random_number(grid)

# Quitter Pygame
pygame.quit()
