import os
import imageio

# # Set the path to the directory containing the GIF files
# gif_dir = 'Mario/graphics/gifs/openHandgifs'

# # Set the path to the directory where you want to save the PNG files
# png_dir = 'Mario/graphics/gifs/openHandPng'

# # Get a list of all the GIF files in the directory
# gif_files = [f for f in os.listdir(gif_dir) if f.endswith('.gif')]

# # Loop through the GIF files and convert each one to PNG format
# for gif_file in gif_files:
#     gif_path = os.path.join(gif_dir, gif_file)
#     png_path = os.path.join(png_dir, gif_file.replace('.gif', '.png'))
#     with imageio.get_reader(gif_path) as reader:
#         frames = reader.get_data()
#     imageio.mimsave(png_path, frames, 'PNG')




from PIL import Image, ImageSequence
import os

input_dir = 'Mario/graphics/gifs/rightHandGifs'
output_dir = 'Mario/graphics/gifs/rightHandPng'

# Loop through the input directory and convert all GIFs to PNGs
for filename in os.listdir(input_dir):
    if filename.endswith('.gif'):
        # Load the GIF using Pillow
        gif_path = os.path.join(input_dir, filename)
        gif = Image.open(gif_path)

        # Loop through each frame and save as a PNG
        for i in range(gif.n_frames):
            gif.seek(i)
            png_path = os.path.join(output_dir, f"{filename}_{i}.png")
            gif.save(png_path)

        # Close the GIF
        gif.close()

print('Conversion complete')
