import os
from PIL import Image

def downscale_to_hd(image_path):
    # Open the image using PIL
    img = Image.open(image_path)

    # Check if the image is already in HD resolution
    if img.size == (1920, 1080):
        print(f"Image {image_path} is already in HD resolution.")
        return

    # Calculate the scaling factor for maintaining aspect ratio
    width, height = img.size
    aspect_ratio = width / height
    new_width = 1920
    new_height = int(new_width / aspect_ratio)

    # Resize the image while maintaining aspect ratio
    resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)

    # Create a blank white background canvas in HD resolution
    background = Image.new('RGB', (1920, 1080), (255, 255, 255))

    # Calculate the position to paste the resized image at the center
    x = (background.width - resized_img.width) // 2
    y = (background.height - resized_img.height) // 2

    # Paste the resized image onto the background canvas
    background.paste(resized_img, (x, y))

    # Save the downscaled image
    output_path = os.path.splitext(image_path)[0] + "_ds.jpg"
    background.save(output_path)
    print(f"Image {image_path} downscaled to HD resolution and saved as {output_path}.")

    # Delete the original image
    os.remove(image_path)
    print(f"Original image {image_path} deleted.")

# Specify the directory path containing the images
image_directory = "/content/ECON/examples"

# Iterate over each file in the directory
for filename in os.listdir(image_directory):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # Construct the full path to the image file
        image_path = os.path.join(image_directory, filename)

        # Downscale the image to HD resolution and delete the original
        downscale_to_hd(image_path)

