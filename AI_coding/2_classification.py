import pygame
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Settings
GRID_SIZE = 20
PIXEL_SIZE = 20
SCREEN_SIZE = GRID_SIZE * PIXEL_SIZE
BG_COLOR = (255, 255, 255)
DRAW_COLOR = (0, 0, 0)
DATA_FILE = "2_drawings_dataset.csv"

# Pygame init
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Draw to Predict")
clock = pygame.time.Clock()

# Drawing grid
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)


def draw_grid():
    screen.fill(BG_COLOR)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y, x] == 1:
                rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
                pygame.draw.rect(screen, DRAW_COLOR, rect)
    pygame.display.flip()


def get_drawing_input():
    global grid
    running = True
    while running:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                gx, gy = x // PIXEL_SIZE, y // PIXEL_SIZE
                if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
                    grid[gy, gx] = 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
                    print("Cleared")

        clock.tick(240)
    return grid.flatten()


def load_data():
    df = pd.read_csv(DATA_FILE)
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    return X, y


def train_model(X, y):
    model = RandomForestClassifier()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"✅ Training accuracy: {acc * 100:.2f}%")
    return model


# Pipeline
X, y = load_data()
model = train_model(X, y)

print("\n🎨 Draw something! Press Enter to finish and let the model guess.")
drawing = get_drawing_input()
prediction = model.predict([drawing])[0]
print(f"\n🤖 I think you drew: **{prediction}**")

pygame.quit()
