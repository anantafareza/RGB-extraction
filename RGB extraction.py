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
    
    print(f"Image: {image_path}, Average Color: {avg_color_rgb}, Interpolated pH Value: {pH_value}")
    return pH_value

def plot_pH_changes(pH_values, reference_colors):
    if not pH_values:
        print("No pH values to plot.")
        return
    
    fig, ax = plt.subplots(figsize=(1.23725, 2.8925))

    for label, values in pH_values.items():
        # Convert the reference color for the current dataset
        reference_rgb = np.array(hex_to_rgb(reference_colors[label])) 
        reference_pH = interpolate_pH(reference_rgb)

        times = [timestamp for timestamp, _ in values]
        pH_values = [pH_value for _, pH_value in values]
        delta_pH = [pH - reference_pH for pH in pH_values]
        ax.scatter(times, delta_pH, s=10, label=f'{label} points')
        ax.plot(times, delta_pH, linewidth=1, linestyle='-', label=f'{label} line')

    ax.set_xlabel('t / s')
    ax.set_ylabel('Average ΔpH')

    # Set exact axis limits
    ax.set_xlim(-4, 64)
    ax.set_ylim(-0.02, 0.32)

    # Minor ticks
    ax.set_xticks(np.arange(0, 60.1, 20))
    ax.set_yticks(np.arange(0, 0.33, 0.1))
    ax.set_xticks(np.arange(0, 60.1, 4), minor=True) 
    ax.set_yticks(np.arange(-0.02, 0.33, 0.02), minor=True) 

    ax.tick_params(axis='x', which='both', labelsize=8, width=1)
    ax.tick_params(axis='y', which='both', labelsize=8, width=1)
    ax.tick_params(axis='x', which='major', length=2, direction='in', top=True)
    ax.tick_params(axis='x', which='minor', length=1, direction='in', top=True)
    ax.tick_params(axis='y', which='major', length=2, direction='in', right=True)
    ax.tick_params(axis='y', which='minor', length=1, direction='in', right=True)

    for spine in ax.spines.values():
        spine.set_linewidth(1)

    # Display the legend
    ax.legend(frameon=False, facecolor='none', fontsize=8)

    plt.show()

# Example usage
frame_times = [0, 10, 20, 30, 40, 50, 60]  # Timestamps of your frames in seconds
rpm_conditions = ['0 rpm', '500 rpm', '1000 rpm', '1500 rpm']
reference_colors = {
    '0 rpm': '18cf32ff',
    '500 rpm': '17ce46ff',
    '1000 rpm': '17d031ff',
    '1500 rpm': '17cf3eff'
}  # Set your desired reference colors for each dataset 

pH_values = {rpm: [] for rpm in rpm_conditions}

for rpm in rpm_conditions:
    for time in frame_times:
        image_path = f'[FILE PATH]{rpm}_trimmed_frame_{time}s.tif'
        pH_value = analyze_pH_change(image_path)
        if pH_value is not None:
            pH_values[rpm].append((time, pH_value))

# Output pH values
for rpm, values in pH_values.items():
    for timestamp, pH_value in values:
        print(f"{rpm}, Time = {timestamp}s: pH value = {pH_value}")

plot_pH_changes(pH_values, reference_colors)
