from IPython.display import Image as IPImage, display
import cv2
import os

def dimages_google_colab(folder_path):
    # Get a list of all image files in the specified folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        # Display the image name without extension
        print(os.path.splitext(image_file)[0])

        # Display the image using IPython.display
        display(IPImage(filename=os.path.join(folder_path, image_file), width=600))

def display_images_cv(folder_path):
    # Get a list of all image files in the specified folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        # Read the image using OpenCV
        image_path = os.path.join(folder_path, image_file)
        img = cv2.imread(image_path)

        # Resize the image (optional)
        img = cv2.resize(img, (512,512))

        # Display the image
        cv2.imshow(os.path.splitext(image_file)[0], img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

