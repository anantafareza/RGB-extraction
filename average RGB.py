import cv2
import numpy as np

# Function to calculate the average color of an image and convert it to hex
def calculate_average_color_hex(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image file {image_path}.")
        return None
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    avg_color = np.mean(image_rgb, axis=(0, 1))
    avg_color_rgb = avg_color[:3]  # No need to divide by 255 for hex conversion
    
    # Convert to hexadecimal
    avg_color_hex = ''.join([f'{int(c):02x}' for c in avg_color_rgb])
    
    print(f"Image: {image_path}, Average Color (Hex): #{avg_color_hex}")
    return avg_color_hex

# List of images
image_paths = [
    '[FILE PATH]'
]

# Calculate the average color for each image and convert to hex
average_colors = {}
for path in image_paths:
    avg_color_hex = calculate_average_color_hex(path)
    if avg_color_hex is not None:
        average_colors[path] = avg_color_hex

# Output the average colors in hex
for path, color in average_colors.items():
    print(f"Average color for {path}: #{color}")
