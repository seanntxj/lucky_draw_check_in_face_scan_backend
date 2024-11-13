'''
Converts images from any format to jpg. Preserves folder structure.
Mainly used as a utility function for the old image training dataset.
'''

from PIL import Image
import os

def convert_images_to_jpg(source_folder, output_folder):
    """Converts images in source_folder to JPG and saves them to output_folder, preserving folder structure."""

    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"Source folder '{source_folder}' not found.")

    os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist

    for root, _, files in os.walk(source_folder):
        relative_path = os.path.relpath(root, source_folder)
        output_subdir = os.path.join(output_folder, relative_path)
        os.makedirs(output_subdir, exist_ok=True)  # Create subdirectories in output folder

        for file in files:
            if file.lower().endswith(('.png', '.jpeg', '.jpg', '.gif', '.bmp')): #add more extensions if needed
                try:
                    img_path = os.path.join(root, file)
                    img = Image.open(img_path)
                    
                    # Extract orientation EXIF data and rotate accordingly
                    exif = img.getexif()
                    orientation = exif.get(0x112, 1)  # 0x112 is the EXIF tag for orientation
                    
                    rotation_mapping = {
                        3: 180,
                        6: 270,
                        8: 90,
                    }
                    
                    img = img.rotate(rotation_mapping.get(orientation, 0), expand=True)

                    # Convert to RGB if the image has an alpha channel
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    output_img_path = os.path.join(output_subdir, file[:-4] + ".jpg") #remove extension and add .jpg
                    img.save(output_img_path, "JPEG")
                    # print(f"Converted '{img_path}' to '{output_img_path}'")
                except IOError as e:
                    print(f"Error processing '{img_path}': {e}")
                except Exception as e:
                    print(f"An unexpected error occurred while processing '{img_path}': {e}")


convert_images_to_jpg('./faces', './faces_2')