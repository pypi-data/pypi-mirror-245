import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import matplotlib.colors as mcolors
import numpy as np

def hexagon(x_center, y_center, size):
    """Generate the coordinates for a hexagon rotated by 90 degrees."""
    return [(x_center + size * sin(theta), y_center + size * cos(theta))
            for theta in [i * (2 * pi / 6) for i in range(6)]]

# Initialize the plot
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.axis('off')

from math import sin, cos, pi

# Parameters
radius = 1.0
horizontal_spacing = 3 * radius
vertical_spacing = 2.75 * radius
base_color=np.array(list(mcolors.to_rgba('xkcd:bright green')))
values = list(range(100, -1, -10))

def compute_centered_x_start(num_hexagons):
    total_width_for_hexagons = num_hexagons * horizontal_spacing - radius
    return -(total_width_for_hexagons / 2)

x, y = compute_centered_x_start(5), 0  # Start with assumption of 5 hexagons for the first row

for idx, value in enumerate(values):
    hex_coords = hexagon(x, y, radius)
    
    # Convert the value (0-100) to a value between 0 and 1
    fuel_content = value / 100.0
    color = base_color * fuel_content
    
    hex_patch = patches.Polygon(hex_coords, facecolor=color, edgecolor='black')
    ax.add_patch(hex_patch)
    
    # Add label
    ax.text(x, y - 1.5 * radius, f"{value}% fuel", ha='center', va='center', fontsize=8)

    # Update x, y for next hexagon
    if (idx + 1) % 5 == 0:
        remaining_hexagons = len(values) - (idx + 1)
        x = compute_centered_x_start(min(5, remaining_hexagons))
        y -= vertical_spacing
    else:
        x += horizontal_spacing

ax.autoscale_view()
plt.show()
