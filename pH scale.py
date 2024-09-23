import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

# Set the font to Arial
plt.rcParams['font.family'] = 'Arial'

# Load the LUT from the CSV file
lut_csv_path = r'[FILE PATH]'

# Read the CSV file and skip any rows with non-numeric values
df = pd.read_csv(lut_csv_path, header=None)

# Filter out non-numeric rows
df = df.apply(pd.to_numeric, errors='coerce').dropna()

# Skip the first column and convert the RGB values to float
rgb_values = df.iloc[:, 1:4].values / 255.0

# Create the custom colormap
physics_cmap = LinearSegmentedColormap.from_list('physics_lut', rgb_values, N=256)

# Set the size of the figure
fig, ax = plt.subplots(figsize=(5.08, 0.25))  # Adjusted for horizontal orientation

# Create a gradient from 3 to 11 for the x-axis
x = np.linspace(3, 11, 256).reshape(1, -1)
y = np.array([0, 1])

# Plot the gradient with the custom 'Physics' colormap
ax.imshow(x, aspect='auto', cmap=physics_cmap, extent=[3, 11, 0, 1])

# Adjust the x-axis scale
ax.set_xlim(3, 11)

# Remove y-axis labels and ticks
ax.set_yticks([])
ax.set_yticklabels([])

# Set the x-axis ticks and label on the bottom side
ax.set_xticks(np.arange(3, 11.1, 1))
ax.set_xticks(np.arange(3, 11.1, 0.2), minor=True)
ax.set_xlabel('pH scale')

# Enable ticks on the bottom axes
ax.tick_params(axis='x', which='both', labelsize=8, width=1)
ax.tick_params(axis='x', which='major', length=2, direction='in', top=False)
ax.tick_params(axis='x', which='minor', length=1, direction='in', top=False)

# Set the line width of the plot box
for spine in ax.spines.values():
    spine.set_linewidth(1)

# Show the plot
plt.show()
