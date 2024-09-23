import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.spatial import distance

# Set the font to Arial
plt.rcParams['font.family'] = 'Arial'

# Define color to pH mapping
color_to_pH = {
    'e92210ff': 3,
    'e38712ff': 4,
    'cfdd13ff': 5,
    '60d615ff': 6,
    '18cc6eff': 7,
    '19b1c4ff': 8,
    '1552baff': 9,
    '00019aff': 10,
    '2f0277ff': 11
}

# Convert hex color to RGB
def hex_to_rgb(hex_color):
    return mcolors.hex2color('#' + hex_color)

# Interpolate pH values based on the color
def interpolate_pH(color_rgb):
    pH_values = list(color_to_pH.values())
    hex_colors = list(color_to_pH.keys())
    rgb_colors = [np.array(hex_to_rgb(c)) for c in hex_colors]

    color_rgb = np.array(color_rgb)
    distances = [distance.euclidean(color_rgb, rgb) for rgb in rgb_colors]
    min_idx = np.argmin(distances)
    if min_idx == 0:
        return pH_values[0]
    elif min_idx == len(pH_values) - 1:
        return pH_values[-1]
    else:
        pH1, pH2 = pH_values[min_idx - 1], pH_values[min_idx]
        rgb1, rgb2 = rgb_colors[min_idx - 1], rgb_colors[min_idx]
        ratio = np.linalg.norm(color_rgb - rgb1) / np.linalg.norm(rgb2 - rgb1)
        return pH1 + ratio * (pH2 - pH1)

def analyze_pH_change(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image file {image_path}.")
        return None
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    avg_color = np.mean(image_rgb, axis=(0, 1))
    avg_color_rgb = avg_color[:3] / 255.0

    pH_value = interpolate_pH(avg_color_rgb)
    
    print(f"Image: {image_path}, Average Color: {avg_color_rgb}, Interpolated pH Value: {pH_value}")  # Debug statement
    return pH_value

def plot_pH_changes(pH_values):
    if not pH_values:
        print("No pH values to plot.")
        return
    
    fig, ax = plt.subplots(figsize=(3.5, 2))

    # Plot pH values
    times = [pH for pH, _ in pH_values]
    pH_values_list = [pH_value for _, pH_value in pH_values]

    ax.scatter(times, pH_values_list, s=10, label='pH points')
    ax.plot(times, pH_values_list, linewidth=1, linestyle='-', label='pH line')

    ax.set_xlabel('pH Value')
    ax.set_ylabel('Measured pH')

    # Set exact axis limits
    ax.set_xlim(2.8, 11.2)
    ax.set_ylim(2.8, 11.2)

    # Minor ticks
    ax.set_xticks(np.arange(3, 12, 1))
    ax.set_yticks(np.arange(3, 12, 1))
    ax.set_xticks(np.arange(2.8, 11.2, 0.2), minor=True)
    ax.set_yticks(np.arange(2.8, 11.2, 0.2), minor=True)

    ax.tick_params(axis='x', which='both', labelsize=8, width=1)
    ax.tick_params(axis='y', which='both', labelsize=8, width=1)
    ax.tick_params(axis='x', which='major', length=2, direction='in', top=True)
    ax.tick_params(axis='x', which='minor', length=1, direction='in', top=True)
    ax.tick_params(axis='y', which='major', length=2, direction='in', right=True)
    ax.tick_params(axis='y', which='minor', length=1, direction='in', right=True)

    for spine in ax.spines.values():
        spine.set_linewidth(1)

    # Save the plot as an EPS file
    plt.savefig('pH_values_plot.eps', format='eps', bbox_inches='tight')

    # Display the legend
    ax.legend(frameon=False, facecolor='none', fontsize=8)

    plt.show()

# Example usage
frame_pHs = [3, 5, 7, 9, 11]  # pH values represented by the files

pH_values = []

for pH in frame_pHs:
    image_path = f'[FILE PATH]'
    pH_value = analyze_pH_change(image_path)
    if pH_value is not None:
        pH_values.append((pH, pH_value))

# Output pH values
for pH, pH_value in pH_values:
    print(f"pH = {pH}: Measured pH value = {pH_value}")

plot_pH_changes(pH_values)
