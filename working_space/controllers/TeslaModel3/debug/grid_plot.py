
import numpy as np
import matplotlib.pyplot as plt

color_map = {
    '0': (255/255, 255/255, 255/255),  # White for empty space
    '1': (211/255, 211/255, 211/255),  # Light silver for sidewalk
    '5': (220/255, 220/255, 220/255),  # Light gray for low buildings
    '6': (211/255, 211/255, 211/255),  # Middle range gray for middle buildings
    '7': (200/255, 200/255, 200/255),  # Darker gray for middle buildings
    '8': (192/255, 192/255, 192/255),  # Dark gray for tall buildings
    '9': (169/255, 169/255, 169/255),  # Dark gray for tallest buildings
    'M': (0/255, 0/255, 255/255),      # Blue for my vehicle
    'C': (255/255, 165/255, 0/255),    # Orange for other vehicles
    'T': (34/255, 139/255, 34/255),    # Green for trees
    'G': (192/255, 192/255, 192/255),  # Dim silver for guardrails
    'H': (65/255, 41/255, 35/255)      # Brown for humans
}

def convert_to_grid_map(file_path: str):
    with open(file_path, 'r') as file:
        raw_data = file.readlines()
    grid = [list(line.strip()) for line in raw_data]
    image = np.zeros((len(grid), len(grid[0]), 3))
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            image[i, j] = color_map.get(cell, (0, 0, 0))  # Default to black

    return image.reshape(len(grid), len(grid[0]))



def grid_plot(image):
    # image = convert_to_grid_map(file_path)
    plt.figure(figsize=(12, 12))
    plt.imshow(image, origin='lower', cmap='gray')

    plt.xlabel("X-axis (grid)")
    plt.ylabel("Y-axis (grid)")
    plt.title("Grid Map Visualization")
    plt.show()


