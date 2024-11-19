import os
import shutil
from PIL import Image

def create_placeholder_image(file_path):
    """Create a 1x1 white JPEG image at the specified path."""
    img = Image.new("RGB", (1, 1), "white")
    img.save(file_path, "JPEG")

def copy_structure_with_placeholders(src, dest):
    """
    Copy the file structure from src to dest, replacing image files with
    1x1 white JPEGs.
    """
    if not os.path.exists(src):
        print(f"Source directory '{src}' does not exist.")
        return

    for root, dirs, files in os.walk(src):
        # Create corresponding directory structure in the destination
        relative_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dest, relative_path)
        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(dest_dir, file)

            # Check if the file is an image
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")):
                # Replace image with a placeholder
                dest_file_path = os.path.splitext(dest_file_path)[0] + ".jpg"  # Save as .jpg
                create_placeholder_image(dest_file_path)
                print(f"Replaced image: {src_file_path} -> {dest_file_path}")
            else:
                # Copy non-image files
                shutil.copy2(src_file_path, dest_file_path)
                print(f"Copied file: {src_file_path} -> {dest_file_path}")

# Example usage:
if __name__ == "__main__":
    source_folder = './faces'
    destination_folder = './faces_optimized'
    copy_structure_with_placeholders(source_folder, destination_folder)
