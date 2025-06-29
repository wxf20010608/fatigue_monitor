from PIL import Image
import numpy as np
import cv2

def load_image(image_path):
    """Load an image from the specified path."""
    image = Image.open(image_path)
    return image

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess the image for model input."""
    image = image.resize(target_size)
    image_array = np.array(image) / 255.0  # Normalize to [0, 1]
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

def capture_image_from_camera(camera_index=0):
    """Capture an image from the specified camera."""
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    else:
        raise Exception("Could not capture image from camera.")

def convert_frame_to_image(frame):
    """Convert a frame from OpenCV to PIL Image."""
    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))