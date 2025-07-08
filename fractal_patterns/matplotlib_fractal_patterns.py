import matplotlib.pyplot as plt
import numpy as np
from mpmath import phi


def draw_tree(x, y, angle, branch_len, angle_diff, shorten_factor, min_branch_len, depth=0):
    if branch_len < min_branch_len:
        return

    # Calculate the end point of the branch
    x_end = x + branch_len * np.cos(np.radians(angle))
    y_end = y + branch_len * np.sin(np.radians(angle))

    # Plot the current branch
    plt.plot([x, x_end], [y, y_end], color=(1, abs(0.5 - depth * 0.05), 0), lw=2)  # Color fades as depth increases

    # Recursively draw the two branches symmetrically
    # Keep the same angle difference for both left and right branches
    draw_tree(x_end, y_end, angle - angle_diff, branch_len * shorten_factor, angle_diff, shorten_factor, min_branch_len, depth + 1)
    draw_tree(x_end, y_end, angle + angle_diff, branch_len * shorten_factor, angle_diff, shorten_factor, min_branch_len, depth + 1)


def draw_fractal_cross(x, y, angle, branch_len, angle_diff, shorten_factor, min_branch_len, depth=0, branch_angle=0):
    if branch_len < min_branch_len:
        return

    # Calculate the end point of the branch
    x_end = x + branch_len * np.cos(np.radians(angle + branch_angle))
    y_end = y + branch_len * np.sin(np.radians(angle + branch_angle))

    # Plot the current branch
    color = (1, abs(0.5 - depth) * 0.05, 0)  # Color fades as depth increases
    plt.plot([x, x_end], [y, y_end], color=color, lw=2)

    # Recursively draw the branches with golden spiral influence and Mandelbrot-inspired structure
    new_angle_diff = angle_diff * np.cos(np.radians(depth * 15))  # Dynamically changing angle difference
    new_branch_len = branch_len * shorten_factor * (phi ** -depth)  # Shrinking influenced by golden ratio

    # For the unfolding cross, add four symmetrical recursive branches
    for angle_shift in [0, 90, 180, 270]:
        draw_fractal_cross(x_end, y_end, angle, new_branch_len, new_angle_diff, shorten_factor, min_branch_len, depth + 1, branch_angle + angle_shift)


def draw_golden_spiral(x, y, angle, branch_len, angle_diff, shorten_factor, min_branch_len, depth=0):
    if branch_len < min_branch_len:
        return

    # Number of points for smooth spiral segment
    num_points = 200
    # The golden angle in radians
    golden_angle_rad = np.radians(137.5)

    # Create angle values for the spiral segment
    theta = np.linspace(0, golden_angle_rad, num_points)
    # Radius follows exponential growth: r = a * e^(b * theta)
    b = 1 / np.tan(golden_angle_rad / 2)
    r = branch_len * np.exp(b * theta)

    # Convert polar to Cartesian
    x_spiral = x + r * np.cos(theta + np.radians(angle))
    y_spiral = y + r * np.sin(theta + np.radians(angle))

    # Plot the spiral segment
    plt.plot(x_spiral, y_spiral, color=(1, abs(0.5 - 0.05 * depth), 0), lw=2)

    # Get end point of spiral to continue from there
    x_end = x_spiral[-1]
    y_end = y_spiral[-1]
    new_angle = angle + 137.5
    new_branch_len = branch_len * shorten_factor

    # Recursive call for the next arc
    draw_golden_spiral(x_end, y_end, new_angle, new_branch_len, angle_diff, shorten_factor, min_branch_len, depth + 1)


def create_fractal_tree():
    # Set up the plot
    plt.figure(figsize=(7, 7))
    plt.axis('off')  # Hide axes

    # Starting position and parameters
    x_start, y_start = 0, 0
    angle = 90  # Start facing upwards
    angle_diff = 25  # Angle difference between left and right branches
    shorten_factor = 0.75  # Slower branch length reduction
    min_branch_len = 1  # Minimum length for recursion to stop

    # Draw the pattern starting from the base:

    draw_tree(x_start, y_start, angle, 20, angle_diff, shorten_factor, min_branch_len)
    # draw_fractal_cross(x_start, y_start, angle, 2000, angle_diff, shorten_factor, min_branch_len)
    # draw_golden_spiral(x_start, y_start, angle, 20, angle_diff, shorten_factor, min_branch_len)

    # Display the plot
    plt.show()


# Create and display the fractal tree
create_fractal_tree()
