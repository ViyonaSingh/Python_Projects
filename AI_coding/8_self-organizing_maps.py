import pygame
import numpy as np
import matplotlib.pyplot as plt
from minisom import MiniSom
from scipy.interpolate import interp1d
from matplotlib.animation import FuncAnimation, PillowWriter

# === Drawing Config ===
WIDTH, HEIGHT = 400, 400
N_POINTS = 1000
STEPS = 30
SHOW_SOM_LINE = False  # Set to "false" to hide the red SOM line


def draw_shape(title):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title)
    screen.fill((255, 255, 255))
    points = []
    drawing = True
    while drawing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drawing = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(screen, (0, 0, 0), pos, 2)
                points.append(pos)
        pygame.display.flip()
    pygame.quit()

    if len(points) < 2:
        return np.zeros((N_POINTS, 2))

    points = np.array(points)
    points[:, 1] = HEIGHT - points[:, 1]  # Flip Y-axis
    normalized = (points - [WIDTH / 2, HEIGHT / 2]) / (WIDTH / 2)
    return resample_shape(normalized, N_POINTS)


def resample_shape(points, n_points):
    dists = np.cumsum(np.linalg.norm(np.diff(points, axis=0), axis=1))
    dists = np.insert(dists, 0, 0)
    f = interp1d(dists, points, axis=0, kind='linear')
    uniform_dists = np.linspace(0, dists[-1], n_points)
    return f(uniform_dists)


# === Get Input Shapes ===
print("🎨 Draw Shape A")
shape_a = draw_shape("Draw Shape A")

print("🎨 Draw Shape B")
shape_b = draw_shape("Draw Shape B")

# === Setup matplotlib for animation ===
fig, ax = plt.subplots(figsize=(6, 6))
line, = ax.plot([], [], 'r-', lw=2)
scatter_blended = ax.scatter([], [], c='gray', s=8)
scatter_weights = ax.scatter([], [], c='black', s=12)

ax.axis('equal')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.axis('off')


def update(frame):
    alpha = frame / (STEPS - 1)
    blended = (1 - alpha) * shape_a + alpha * shape_b

    som = MiniSom(1, N_POINTS, 2, sigma=0.2, learning_rate=0.3)
    som.random_weights_init(blended)
    som.train(blended, 300, verbose=False)
    weights = som.get_weights()[0]
    if SHOW_SOM_LINE:
        line.set_data(weights[:, 0], weights[:, 1])
        scatter_weights.set_offsets(weights)
    scatter_blended.set_offsets(blended)
    return line, scatter_weights, scatter_blended


anim = FuncAnimation(fig, update, frames=STEPS, interval=150, blit=True)

# Save as GIF using PillowWriter (make sure pillow is installed)
anim.save("8_morphing.gif", writer=PillowWriter(fps=5))

print("✅ Morphing animation saved as 8_morphing.gif!")

plt.show()
