import os
from shutil import copyfile

def upload_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    
    for image_file in image_files:
        source_path = os.path.join(input_folder, image_file)
        destination_path = os.path.join(output_folder, image_file)
        copyfile(source_path, destination_path)

# Example usage:
upload_images("images", "dataset")
