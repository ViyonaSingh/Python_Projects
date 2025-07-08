import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


def draw_tree(x, y, angle, branch_len, angle_diff, shorten_factor, min_branch_len, depth=0):
    if branch_len < min_branch_len:
        return []
    x_end = x + branch_len * np.cos(np.radians(angle))
    y_end = y + branch_len * np.sin(np.radians(angle))
    branch = [[x, y, x_end, y_end, depth]]
    left = draw_tree(x_end, y_end, angle - angle_diff, branch_len * shorten_factor,
                     angle_diff, shorten_factor, min_branch_len, depth + 1)
    right = draw_tree(x_end, y_end, angle + angle_diff, branch_len * shorten_factor,
                      angle_diff, shorten_factor, min_branch_len, depth + 1)
    return branch + left + right


def create_growing_tree_gif():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-400, 400)
    ax.set_ylim(0, 600)
    ax.axis('off')

    all_branches = draw_tree(0, 0, 90, 150, 25, 0.75, 10)

    lines = []

    def init():
        return []

    def update(frame):
        if frame < len(all_branches):
            x0, y0, x1, y1, depth = all_branches[frame]
            color = (1, max(0, 0.5 - 0.05 * depth), 0)
            line, = ax.plot([x0, x1], [y0, y1], color=color, lw=2)
            lines.append(line)
            return [line]
        return []

    ani = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=len(all_branches),
        interval=30,
        blit=True
    )

    ani.save("growing_tree.gif", writer='pillow', fps=120)
    print("✅ Done! Open growing_tree.gif to see it grow. Make sure you are viewing it with a browser (:")


create_growing_tree_gif()
