import os
import sys
import openslide
from PIL import Image

# Get the input and output directories from command line arguments
if len(sys.argv) != 3:
    print('Usage: python convert_jpg_to_svs.py <input_directory> <output_directory>')
    sys.exit(1)

input_dir = sys.argv[1]
output_dir = sys.argv[2]

# Create the output directory if it does not already exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all .jpg files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.jpg'):
        # Load the .jpg image
        jpg_image = Image.open(os.path.join(input_dir, filename))

        # Convert the .jpg image to RGBA format
        rgba_image = jpg_image.convert('RGBA')

        # Create a new .svs file to save the converted image
        new_slide = openslide.open_slide(os.path.join(output_dir, os.path.splitext(filename)[0] + '.svs'), 'w', rgba_image.width, rgba_image.height, {}, 'svs')

        # Write the image data to the new .svs file
        new_slide.write_region((0, 0), rgba_image.tobytes(), 0)

        # Close the new .svs file
        new_slide.close()

print('All .jpg files in', input_dir, 'have been converted to .svs and saved in', output_dir)
