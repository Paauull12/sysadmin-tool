import os
from PIL import Image


def resize_images_to_a4(input_image_dir):
    # Define A4 dimensions in points (pixels)
    # Assuming 72 PPI (points per inch)
    A4_WIDTH = 595  # 8.27 inches * 72 points per inch
    A4_HEIGHT = 842  # 11.69 inches * 72 points per inch

    # Iterate through each image in the directory
    for image_filename in sorted(os.listdir(input_image_dir)):
        if image_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            image_path = os.path.join(input_image_dir, image_filename)
            image = Image.open(image_path)
            width, height = image.size

            # Calculate scaling factors to fit A4
            scale_x = A4_WIDTH / width
            scale_y = A4_HEIGHT / height

            # Use the smaller scale to ensure the entire image fits within A4
            scale = min(scale_x, scale_y)

            # Ensure scale is not below the minimum scale
            min_scale = 0.3
            if scale < min_scale:
                scale = min_scale
                A4_WIDTH = int(width * scale)
                A4_HEIGHT = int(height * scale)

            # Calculate new dimensions after scaling
            new_width = int(width * scale)
            new_height = int(height * scale)

            # Resize the image
            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

            # Create a new blank A4 image with a white background
            a4_image = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), (255, 255, 255))

            # Calculate position to paste the resized image to center it on A4
            paste_x = (A4_WIDTH - new_width) // 2
            paste_y = (A4_HEIGHT - new_height) // 2

            # Paste the resized image onto the A4 canvas
            a4_image.paste(resized_image, (paste_x, paste_y))

            # Save the A4-sized image back to the original path
            a4_image.save(image_path)
